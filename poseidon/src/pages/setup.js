import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm } from 'antd';
import { PlusOutlined } from '@ant-design/icons'

import { FormButtonModal, FormLinkModal } from '../components';
import { dealWithError, notificate } from '../lib/common';
import { getSetupData, listSetupData, postSetupData, updateSetupData, deleteSetupData } from '../services/aristaeus/setup';
import { ERROR_STATUS, LOADING_STATUS, getGenericPage } from './generic';


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
  state = {tableData: [], pageStatus: LOADING_STATUS, dataType: this.props.dataType}

  getTableData = (data) => {
    const tableData = data.reduce((acc, val, index) => {
      acc.push({
        key: index+1,
        id: val.public_id,
        name: val.value,
      });
      return acc;
    }, []);
    return tableData;
  }

  async componentDidMount() {
    try {
      let data = await listSetupData(this.props.dataType);
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

  postData = async(form) => {
    const value = form.newEntry;

    if (!value) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    try {
      await postSetupData(this.props.dataType, value);
      let data = await listSetupData(this.props.dataType);
      let tableData = this.getTableData(data);
      this.setState((state) => {
        state['tableData'] = tableData;
        return state;
      });
    } catch (error) {
      dealWithError(error);
    }
  }

  updateData = async(form) => {
    const objectId = form.objectId;
    const newValue = form.updateEntry;
    const oldValue = form.oldValue;

    if (newValue === undefined || newValue === oldValue) {
      notificate('error', window.i18n('error.sameEntry'))
      return;
    }

    if (!newValue) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    try {
      await updateSetupData(newValue, objectId);
      let data = await listSetupData(this.props.dataType);
      let tableData = this.getTableData(data);
      this.setState((state) => {
        state['tableData'] = tableData;
        return state;
      });
    } catch (error) {
      dealWithError(error);
    }
  }

  deleteData = async(objectId) => {
    try {
      await deleteSetupData(objectId);
      let data = await listSetupData(this.props.dataType);
      let tableData = this.getTableData(data);
      this.setState((state) => {
        state['tableData'] = tableData;
        return state;
      });
    } catch (error) {
      dealWithError(error);
    }
  }

  render() {
    console.log(this.state);
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

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
              <Button type="link">{window.i18n('word.delete')}</Button>
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
            <FormButtonModal title={window.i18n("title.addNewEntry")} formId='addNewDataFormId' buttonIcon={<PlusOutlined />}>
              <AddNewDataForm dataType={this.props.dataType} onFinish={this.postData} />
            </FormButtonModal>
          </Col>
        </Row>
      </>
    )
  }
}