import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select, Divider } from 'antd';
import { PlusOutlined } from '@ant-design/icons'
import { navigate } from '@reach/router';

import { FormButtonModal, FormLinkModal } from '../../components';
import { dealWithError, notificate } from '../../lib/common';
import { formItemLayout, tailFormItemLayout } from '../../constants';

import { getSetupData } from '../../services/aristaeus/setup';
import { createApiary, getApiaries, updateApiary, deleteApiary } from '../../services/aristaeus/apiary';
import { NOT_FOUND_STATUS, ERROR_STATUS, LOADING_STATUS, getGenericPage } from '../generic';


function onFailed(err) {
  notificate("error", "Failed")
}

export function UpdateApiaryForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "apiaryId": props.apiaryId,
    "name": props.record.name,
    "location": props.record.location,
    "honey_type": props.record.honeyTypeId,
  })

  return (
    <Form {... formItemLayout} id="updateApiaryFormId" form={form} name="basic" onFinish={props.onFinish} onFinishFailed={onFailed}>
      <Form.Item label={window.i18n("word.name")} name="name" rules={[{type: 'string', min: 1, message: window.i18n('form.insertApiaryName')}]}>
        <Input defaultValue={props.record.name} />
      </Form.Item>
      <Form.Item label={window.i18n("word.location")} name="location" rules={[{type: 'string', min: 1, message: window.i18n('form.insertApiaryLocation')}]}>
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
  state = {tableData: [], apiaryHoneyType: [], pageStatus: LOADING_STATUS}

  getTableContent = (data) => {
    const tableData = data.reduce((acc, val, index) => {
        acc.push({
          key: index+1,
          id: val.id,
          name: val.name,
          location: val.location,
          honeyType: val.honey_type.name,
          honeyTypeId: val.honey_type.id,
          nb_hives: val.nb_hives,
        });
        return acc;
      }, []);

    return tableData;
  }

  async componentDidMount() {
    try {
      let apiaries = await getApiaries();
      let apiaryHoneyType = await getSetupData('apiary_honey_type');
      let tableData = this.getTableContent(apiaries);
      let pageStatus = 'OK';

      this.setState({tableData, apiaryHoneyType, pageStatus})

    } catch (error) {
      dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = ERROR_STATUS;
      })
    }
  }

  deleteData = async(apiaryId) => {
    try {
      await deleteApiary(apiaryId);
      let apiaries = await getApiaries();
      let tableData = this.getTableContent(apiaries);

      this.setState((state) => {
        state['apiaries'] = apiaries;
        state['tableData'] = tableData;
        return state;
      })
    } catch (error) {
      dealWithError(error);
    }
  }

  updateData = async(form) => {
    const apiaryId = form.apiaryId
    const data = {
      name: form.name,
      location: form.location,
      honey_type_id: form.honey_type
    }

    try {
      await updateApiary(apiaryId, data);
      let apiaries = await getApiaries();
      let tableData = this.getTableContent(apiaries);

      this.setState((state) => {
        state['apiaries'] = apiaries;
        state['tableData'] = tableData;
        return state;
      })
    } catch (error) {
      dealWithError(error);
    }
  }

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

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
        title: window.i18n('word.hives'),
        dataIndex: 'nb_hives',
        key: 'nb_hives',
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
              <UpdateApiaryForm apiaryId={record.id} record={record} honey_types={this.state.apiaryHoneyType} onFinish={this.updateData} />
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
    pageStatus: LOADING_STATUS,
    apiaryHoneyType: []
  }

  async componentDidMount() {
    try {
      let apiaryHoneyType = await getSetupData('apiary_honey_type');
      let pageStatus = 'OK';

      this.setState({apiaryHoneyType, pageStatus})
    } catch (error) {
      dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = ERROR_STATUS;
        return state;
      })
    }
  }

  async postData(data) {
    try {
      await createApiary(data);
      navigate('/manage/apiary');
    } catch (error) {
      dealWithError(error);
    }
  }

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

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
                    this.state['apiaryHoneyType'].map(data => {
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