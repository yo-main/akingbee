import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select } from 'antd';
import { PlusOutlined } from '@ant-design/icons'

import { FormButtonModal, FormLinkModal } from '../../components';
import { notificate } from '../../lib/common'

import { getSetupData } from '../../services/aristaeus/setup';
import { createApiary } from '../../services/aristaeus/apiary';
import { navigate } from '@reach/router';


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


export class ApiaryPage extends React.Component {
  state = {tableData: []}

  render() {

    const columns = [
      {
        title: window.i18n('word.name'),
        dataIndex: 'name',
        key: 'name',
        defaultSortOrder: 'ascend',
        sorter: (a, b) => a.name.localeCompare(b.name),
      },
      {
        title: window.i18n('word.location'),
        dataIndex: 'location',
        key: 'location',
      },
      {
        title: window.i18n('word.status'),
        dataIndex: 'status',
        key: 'status',
      },
      {
        title: window.i18n('word.honeyType'),
        dataIndex: 'honeyType',
        key: 'honeyType',
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
    ]

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





export class ApiaryCreationPage extends React.Component {
  state = {
    apiary_status: [],
    apiary_honey_type: []
  }

  refreshState = ({data, type}) => {
    this.setState((state) => {
      state[type] = data;
      return state;
    })
    console.log(this.state);
  }

  componentDidMount() {
    getSetupData('apiary_status', this.refreshState);
    getSetupData('apiary_honey_type', this.refreshState);
  }

  postData(data) {
    createApiary(data, () => navigate('/manage/apiary'));
  }

  render() {

    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
      },
    };

    const tailFormItemLayout = {
      wrapperCol: {
        xs: {
          span: 24,
          offset: 0,
        },
        sm: {
          span: 16,
          offset: 8,
        },
      },
    };

    return (
      <>
        <Row>
          <Col push={3}>
            <h1>{window.i18n('title.apiaryCreation')}</h1><br/>
          </Col>
        </Row>
        <Row>
          <Col push={1}>
            <Form {...formItemLayout} onFinish={this.postData} onFinishFailed={onFailed} requiredMark={false}>
              <Form.Item label={window.i18n("word.name")} name="name" rules={[{required: true}]}>
                <Input />
              </Form.Item>
              <Form.Item label={window.i18n("word.location")} name="location" rules={[{required: true}]}>
                <Input />
              </Form.Item>
              <Form.Item label={window.i18n("word.status")} name="status" rules={[{required: true}]}>
                <Select defaultValue={window.i18n('form.selectAValue')}>
                  {
                    this.state['apiary_status'].map(data => {
                      return (
                        <Select.Option key={data.id}>{data.name}</Select.Option>
                      )
                    })
                  }
                </Select>
              </Form.Item>
              <Form.Item label={window.i18n("word.honeyType")} name="honey_type" rules={[{required: true}]}>
                <Select defaultValue={window.i18n('form.selectAValue')}>
                  {
                    this.state['apiary_honey_type'].map(data => {
                      return (
                        <Select.Option key={data.id}>{data.name}</Select.Option>
                      )
                    })
                  }
                </Select>
              </Form.Item>
              <Form.Item {... tailFormItemLayout}>
                <Button type="primary" htmlType="submit">
                  Register
                </Button>
              </Form.Item>
            </Form>
          </Col>
        </Row>
      </>
    )
  }
}