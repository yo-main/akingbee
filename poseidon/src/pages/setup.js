import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm } from 'antd';
import { PlusOutlined } from '@ant-design/icons'

import { FormButtonModal, FormLinkModal } from '../components';
import { notificate } from '../lib/common';
import { getSetupData, postSetupData, updateSetupData, deleteSetupData } from '../services/aristaeus/setup';


function onFailed(err) {
  notificate("error", "Failed")
}

export function AddNewDataForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "dataType": props.dataType,
  })

  return (
    <Form id="addNewDataFormId" form={form} name="basic" onFinish={props.onFinish} onFinishFailed={onFailed}>
      <Form.Item label={window.i18n("form.newEntry")} name="newEntry">
        <Input />
      </Form.Item>
      <Form.Item name="dataType" hidden={true}/>
    </Form>
  )
}

export function UpdateDataForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "dataType": props.dataType,
    "oldValue": props.currentValue,
    "objectId": props.objectId,
  })

  return (
    <Form id="updateDataFormId" form={form} name="basic" onFinish={props.onFinish} onFinishFailed={onFailed}>
      <Form.Item label={window.i18n("form.updateEntry")} name="updateEntry">
        <Input defaultValue={props.currentValue} />
      </Form.Item>
      <Form.Item name="dataType" hidden={true} />
      <Form.Item name="oldValue" hidden={true} />
      <Form.Item name="objectId" hidden={true} />
    </Form>
  )
}


export class SetupPage extends React.Component {
  state = {tableData: []}

  refreshState = ({data}) => {
    const tableData = data.reduce((acc, val, index) => {
      acc.push({
        key: index+1,
        id: val.id,
        name: val.name,
      });
      return acc;
    }, []);
    this.setState((state) => ({tableData}));
  }

  refreshData = () => {
    getSetupData(this.refreshState, this.props.dataType);
  }

  componentDidMount() {
    this.refreshData();
  }

  postData = (form) => {
    const value = form.newEntry;

    if (!value) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    postSetupData(this.props.dataType, value, this.refreshData);
  }

  updateData = (form) => {
    const objectId = form.objectId;
    const newValue = form.updateEntry;
    const oldValue = form.oldValue;

    console.log("onFinish", newValue, oldValue, form)

    if (newValue === undefined || newValue === oldValue) {
      notificate('error', window.i18n('error.sameEntry'))
      return;
    }

    if (!newValue) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    updateSetupData(this.props.dataType, newValue, objectId, this.refreshData);
  }

  deleteData = (objectId) => {
    deleteSetupData(this.props.dataType, objectId, this.refreshData);
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
      {
        title: window.i18n('word.actions'),
        key: 'action',
        render: (text, record) => (
          <Space size='middle'>
            <FormLinkModal title={window.i18n('title.updateEntry')} formId='updateDataFormId' linkContent={window.i18n('word.edit')}>
              <UpdateDataForm objectId={record.id} currentValue={record.name} dataType={this.props.dataType} onFinish={this.updateData} />
            </FormLinkModal>
            <Popconfirm onConfirm={() => this.deleteData(record.id)} title={window.i18n("confirm.deleteData")}>
              <a href='#'>{window.i18n('word.delete')}</a>
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
          <Col style={{ paddingLeft: '20px'}}>
            <FormButtonModal title={window.i18n("title.addNewEntry")} formId='addNewDataFormId' buttonContent={<PlusOutlined />}>
              <AddNewDataForm dataType={this.props.dataType} onFinish={this.postData} />
            </FormButtonModal>
          </Col>
        </Row>
      </>
    )
  }
}