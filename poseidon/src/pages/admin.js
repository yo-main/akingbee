import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm } from 'antd';
import { PlusOutlined } from '@ant-design/icons'

import { FormButtonModal, FormLinkModal } from '../components';
import { dealWithError, notificate } from '../lib/common';
import { getAllUsers, impersonateRequest } from '../services/authentication';
import { ERROR_STATUS, LOADING_STATUS, getGenericPage } from './generic';


function onFailed(err) {
  notificate("error", "Failed")
}

export class AdminPage extends React.Component {
  state = {tableData: [], pageStatus: LOADING_STATUS}

  getTableData = (data) => {
    const tableData = data.reduce((acc, val, index) => {
      acc.push({
        key: index+1,
        id: val.id,
        email: val.email,
        activationId: val.activation_id,
        createdAt: val.created_at,
      });
      return acc;
    }, []);
    return tableData;
  }

  async componentDidMount() {
    try {
      let data = await getAllUsers();
      let tableData = this.getTableData(data.data["users"]);
      let pageStatus = 'OK';

      this.setState({tableData, pageStatus});
    } catch (error) {
      dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = ERROR_STATUS;
        return state;
      })
    }
  }

  impersonate = async(userId) => {
    try {
      impersonateRequest({userId})
    } catch (error) {
      dealWithError(error);
      return
    }
  }

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

    const columns = [
      {
        title: window.i18n(`title.id`),
        dataIndex: 'id',
        key: 'id',
      },
      {
        title: window.i18n(`title.email`),
        dataIndex: 'email',
        key: 'email',
        defaultSortOrder: 'ascend',
        sorter: (a, b) => a.email.localeCompare(b.email),
      },
      {
        title: window.i18n(`title.activationId`),
        dataIndex: 'activationId',
        key: 'activationId',
      },
      {
        title: window.i18n('word.actions'),
        key: 'action',
        render: (text, record) => (
          <Space size='middle'>
            <Popconfirm onConfirm={() => this.impersonate(record.id)} title={window.i18n("confirm.impersonate")}>
              <Button type="link">{window.i18n('word.impersonate')}</Button>
            </Popconfirm>
          </Space>
        )
      }
    ];

    return (
      <>
        <Row>
          <Col offset={2}>
            <Table dataSource={this.state.tableData} columns={columns} pagination={false} bordered />
          </Col>
        </Row>
      </>
    )
  }
}