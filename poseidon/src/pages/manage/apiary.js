import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select, Divider } from 'antd';
import { PlusOutlined } from '@ant-design/icons'

import { FormButtonModal, FormLinkModal } from '../../components';
import { notificate } from '../../lib/common'

import { getSetupData } from '../../services/aristaeus/setup';
import { createApiary, getApiaries, updateApiary, deleteApiary } from '../../services/aristaeus/apiary';
import { navigate } from '@reach/router';


function onFailed(err) {
  notificate("error", "Failed")
}

export function UpdateApiaryForm(props) {
  const formItemLayout = {
    labelCol: {
      xs: { span: 24 },
      sm: { span: 6 },
    },
    wrapperCol: {
      xs: { span: 24 },
      sm: { span: 18 },
    },
  };

  const [form] = Form.useForm();

  form.setFieldsValue({
    "apiaryId": props.apiaryId,
    "name": props.record.name,
    "location": props.record.location,
    "honey_type": props.record.honeyTypeId,
  })

  return (
    <Form {... formItemLayout} id="updateApiaryFormId" form={form} name="basic" onFinish={props.onFinish} onFinishFailed={onFailed}>
      <Form.Item label={window.i18n("word.name")} name="name" rules={[{type: 'string', min: 2, message: window.i18n('form.insertApiaryName')}]}>
        <Input defaultValue={props.record.name} />
      </Form.Item>
      <Form.Item label={window.i18n("word.location")} name="location" rules={[{type: 'string', min: 2, message: window.i18n('form.insertApiaryLocation')}]}>
        <Input defaultValue={props.record.location} />
      </Form.Item>
      <Form.Item label={window.i18n("word.honeyType")} name="honey_type" rules={[{message: window.i18n('form.insertApiaryHoneyType')}]}>
        <Select defaultValue={props.record.honeyTypeId}>
          {
            props.honey_types.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item name="apiaryId" hidden={true} />
    </Form>
  )
}


export class ApiaryPage extends React.Component {
  state = {tableData: [], apiary_honey_type: []}

  refreshApiariesState = ({data}) => {
    const tableData = data.reduce((acc, val, index) => {
        acc.push({
          key: index+1,
          id: val.id,
          name: val.name,
          location: val.location,
          honeyType: val.honey_type.name,
          honeyTypeId: val.honey_type.id,
        });
        return acc;
      }, []);

    this.setState((state) => {
      state.tableData = tableData;
      return state;
    });
  }

  refreshSetupState = ({type, data}) => {
    this.setState((state) => {
      state[type] = data;
      return state;
    })
  }

  componentDidMount() {
    getApiaries(this.refreshApiariesState);
    getSetupData('apiary_honey_type', this.refreshSetupState);
  }

  deleteData = (apiaryId) => {
    deleteApiary(apiaryId, () => getApiaries(this.refreshApiariesState));
  }

  updateData = (form) => {
    const apiaryId = form.apiaryId
    const data = {
      name: form.name,
      location: form.location,
      honey_type_id: form.honey_type
    }
    updateApiary(apiaryId, data, () => getApiaries(this.refreshApiariesState));
  }

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
        title: window.i18n('word.honeyType'),
        dataIndex: 'honeyType',
        key: 'honeyType',
      },
      {
        title: window.i18n('word.actions'),
        key: 'action',
        render: (text, record) => (
          <Space size='middle'>
            <FormLinkModal title={window.i18n('title.apiaryUpdate')} formId='updateApiaryFormId' linkContent={window.i18n('word.edit')}>
              <UpdateApiaryForm apiaryId={record.id} record={record} honey_types={this.state.apiary_honey_type} onFinish={this.updateData} />
            </FormLinkModal>
            <Popconfirm onConfirm={() => this.deleteData(record.id)} title={window.i18n("confirm.deleteApiary")}>
              <a href='#'>{window.i18n('word.delete')}</a>
            </Popconfirm>
          </Space>
        )
      }
    ]

    return (
      <>
        <Row>
          <Col span={23} offset={1}>
            <Table dataSource={this.state.tableData} columns={columns} pagination={false} bordered />
          </Col>
        </Row>
      </>
    )
  }
}



export class ApiaryCreationPage extends React.Component {
  state = {
    apiary_honey_type: []
  }

  refreshState = ({data, type}) => {
    this.setState((state) => {
      state[type] = data;
      return state;
    })
  }

  componentDidMount() {
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
          <Col offset={1}>
            <h1>{window.i18n('title.apiaryCreation')}</h1>
          </Col>
        </Row>
        <Row>
          <Col offset={1} span={23}>
            <Divider style={{paddingLeft: '20px'}} plain/>
            <br/>
          </Col>
        </Row>
        <Row>
          <Col span={8}>
            <Form {...formItemLayout} onFinish={this.postData} requiredMark={false}>
              <Form.Item label={window.i18n("word.name")} name="name" rules={[{required: true, message: window.i18n('form.insertApiaryName')}]}>
                <Input />
              </Form.Item>
              <Form.Item label={window.i18n("word.location")} name="location" rules={[{required: true, message: window.i18n('form.insertApiaryLocation')}]}>
                <Input />
              </Form.Item>
              <Form.Item label={window.i18n("word.honeyType")} name="honey_type" rules={[{required: true, message: window.i18n('form.selectApiaryHoneyType')}]}>
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
                  {window.i18n('word.submit')}
                </Button>
              </Form.Item>
            </Form>
          </Col>
        </Row>
      </>
    )
  }
}