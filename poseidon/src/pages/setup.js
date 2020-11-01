import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input } from 'antd';
import { PlusOutlined } from '@ant-design/icons'

import { FormButtonModal, FormLinkModal } from '../components';
import { notificate } from '../lib/common';
import { getData, postNewData } from '../services/aristaeus/setup';


function onFailed(err) {
  notificate("error", "Failed")
}

export function AddNewData(props) {
  return (
    <Form id="addNewDataFormId" name="basic" onFinish={props.onFinish} onFinishFailed={onFailed}>
      <Form.Item label={window.i18n("form.newEntry")} name="newEntry"
        rules={[{ required: true}]}
      >
        <Input />
      </Form.Item>
      <Form.Item name="dataType" initialValue={props.dataType} hidden={true}/>
    </Form>
  )
}


export class SetupPage extends React.Component {
  state = { tableData: []}

  refreshState = (data) => {
    this.setState((state) => ({tableData: data}));
  }

  refreshData = () => {
    getData(this.props.dataType, this.refreshState);
  }

  componentDidMount() {
    this.refreshData();
  }

  postData = (form) => {
    const value = form.newEntry;
    postNewData(this.props.dataType, value, this.refreshData);
  }

  render() {

    const columns = [
      {
        title: window.i18n(`title.${this.props.dataType}`),
        dataIndex: 'name',
        key: 'name',
        defaultSortOrder: 'ascend',
        sorter: (a, b) => a.name.localeCompare(b.name),
      },
    ];

    columns.push({
      title: window.i18n('word.actions'),
      key: 'action',
      render: (text, record) => (
        <Space size='middle'>
          <FormLinkModal linkContent={window.i18n('word.edit')}></FormLinkModal>
          <FormLinkModal linkContent={window.i18n('word.delete')}></FormLinkModal>
        </Space>
      )
    })

    return (
      <>
        <Row>
          <Col offset={2}>
            <Table dataSource={this.state.tableData} columns={columns} pagination={false} bordered />
          </Col>
          <Col style={{ paddingLeft: '20px'}}>
            <FormButtonModal title={window.i18n("title.addNewEntry")} formId='addNewDataFormId' buttonContent={<PlusOutlined />}>
              <AddNewData dataType={this.props.dataType} onFinish={this.postData} />
            </FormButtonModal>
          </Col>
        </Row>
      </>
    )
  }
}