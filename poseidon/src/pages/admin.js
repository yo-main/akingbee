import React from 'react';

import { Row, Col, Table, Space, Button, Popconfirm } from 'antd';

import { dealWithError } from '../lib/common';
import { getAllUsers, getLoggerUserData, impersonateRequest, desimpersonateRequest } from '../services/authentication';
import { ERROR_STATUS, LOADING_STATUS, getGenericPage } from './generic';


export class AdminPage extends React.Component {
  state = {tableData: [], pageStatus: LOADING_STATUS}

  getTableData = (data) => {

    const tableData = data.reduce((acc, val, index) => {
      acc.push({
        key: index+1,
        id: val.public_id,
        email: val.email,
        activationId: val.activation_id,
        lastSeen: val.last_seen,
      });
      return acc;
    }, []);
    return tableData;
  }

  async componentDidMount() {
    await this.refreshData();
  }

  async refreshData() {
    try {
      let data = await getAllUsers();
      let tableData = this.getTableData(data);
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

    await this.refreshData();
  }

  desimpersonate = async() => {
    try {
      desimpersonateRequest()
    } catch (error) {
      dealWithError(error);
      return
    }

    await this.refreshData();
  }

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

    let userId = getLoggerUserData("user_id");
    let isAdmin = getLoggerUserData("admin");
    let impersonatorId = getLoggerUserData("impersonator_id");

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
        title: window.i18n(`title.lastSeen`),
        dataIndex: 'lastSeen',
        key: 'lastSeen',
      },
      {
        title: window.i18n('word.actions'),
        key: 'action',
        render: (text, record) => {
          let impersonate_action = <></>;
          if (isAdmin && !(record.id === userId || record.id === impersonatorId)) {
            impersonate_action = (
              <Popconfirm onConfirm={() => this.impersonate(record.id)} title={window.i18n("confirm.impersonate")}>
                <Button type="link">{window.i18n('word.impersonate')}</Button>
              </Popconfirm>
            )
          }

          let desimpersonate_action = <></>;
          if (record.id === userId && impersonatorId != null) {
            desimpersonate_action = (
              <Popconfirm onConfirm={() => this.desimpersonate()} title={window.i18n("confirm.desimpersonate")}>
                <Button type="link">{window.i18n('word.desimpersonate')}</Button>
              </Popconfirm>
            )
          }

          return (
            <Space size='middle'>
              {impersonate_action}
              {desimpersonate_action}
            </Space>
          )
        }

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