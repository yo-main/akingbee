import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select, Divider } from 'antd';

import { FormLinkModal } from '../../components';
import { dealWithError, notificate } from '../../lib/common';
import { formItemLayout, tailFormItemLayout } from '../../constants';

import { listSetupData } from '../../services/aristaeus/setup';
import { createApiary, getApiaries, updateApiary, deleteApiary } from '../../services/aristaeus/apiary';
import { LOADING_STATUS, getGenericPage } from '../generic';


function onFailed(err) {
  notificate("error", "Failed")
}

export function UpdateApiaryForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "apiaryId": props.apiaryId,
    "name": props.record.name,
    "location": props.record.location,
    "honey_kind": props.record.honeyKind,
  })

  return (
    <Form {...formItemLayout} id="updateApiaryFormId" form={form} name="basic" onFinish={props.onFinish} onFinishFailed={onFailed}>
      <Form.Item label={window.i18n("word.name")} name="name" rules={[{ type: 'string', min: 1, message: window.i18n('form.insertApiaryName') }]}>
        <Input defaultValue={props.record.name} />
      </Form.Item>
      <Form.Item label={window.i18n("word.location")} name="location" rules={[{ type: 'string', min: 1, message: window.i18n('form.insertApiaryLocation') }]}>
        <Input defaultValue={props.record.location} />
      </Form.Item>
      <Form.Item label={window.i18n("word.honeyKind")} name="honey_kind" rules={[{ message: window.i18n('form.insertApiaryHoneyType') }]}>
        <Select defaultValue={props.record.honeyKind}>
          {
            props.honeyKinds.map(data => {
              return (
                <Select.Option key={data.value}>{data.value}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item name="apiaryId" hidden />
    </Form>
  )
}


export function ApiaryPage(props) {
  const [tableData, setTableData] = React.useState([]);
  const [honeyKinds, setHoneyKinds] = React.useState([]);
  const [pageStatus, setPageStatus] = React.useState(LOADING_STATUS);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        let data = await Promise.all([
          getApiaries(),
          listSetupData('honey_kind'),
        ]);

        setTableData(getTableContent(data[0]));
        setHoneyKinds(data[1]);
        setPageStatus('Ok');

      } catch (error) {
        setPageStatus(dealWithError(error));
      }
    };
    fetchData();
  }, [setTableData, setPageStatus]);

  const getTableContent = (data) => {
    const tableData = data.reduce((acc, val, index) => {
      acc.push({
        key: index + 1,
        id: val.public_id,
        name: val.name,
        location: val.location,
        honeyKind: val.honey_kind,
        nbHives: val.hive_count,
      });
      return acc;
    }, []);

    return tableData;
  }

  const deleteData = async (apiaryId) => {
    try {
      await deleteApiary(apiaryId);
      let apiaries = await getApiaries();
      let tableData = getTableContent(apiaries);
      setTableData(tableData);
    } catch (error) {
      dealWithError(error);
    }
  }

  const updateData = async (form) => {
    const apiaryId = form.apiaryId
    const data = {
      name: form.name,
      location: form.location,
      honey_kind: form.honey_kind
    }

    try {
      await updateApiary(apiaryId, data);
      let apiaries = await getApiaries();
      let tableData = getTableContent(apiaries);
      setTableData(tableData);
    } catch (error) {
      dealWithError(error);
    }
  }

  let genericPage = getGenericPage(pageStatus);
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
      dataIndex: 'nbHives',
      key: 'nbHives',
    },
    {
      title: window.i18n('word.honeyKind'),
      dataIndex: 'honeyKind',
      key: 'honeyKind',
    },
    {
      title: window.i18n('word.actions'),
      key: 'action',
      render: (text, record) => (
        <Space size='middle'>
          <FormLinkModal title={window.i18n('title.apiaryUpdate')} formId='updateApiaryFormId' linkContent={window.i18n('word.edit')}>
            <UpdateApiaryForm apiaryId={record.id} record={record} honeyKinds={honeyKinds} onFinish={updateData} />
          </FormLinkModal>
          <Popconfirm onConfirm={() => deleteData(record.id)} title={window.i18n("confirm.deleteApiary")}>
            <Button type="link">{window.i18n('word.delete')}</Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  return (
    <>
      <Row>
        <Col span={23} offset={1}>
          <Table dataSource={tableData} columns={columns} pagination={false} bordered />
        </Col>
      </Row>
    </>
  )
}


export function ApiaryCreationPage(props) {
  const [pageStatus, setPageStatus] = React.useState(LOADING_STATUS);
  const [honeyKinds, setHoneyKinds] = React.useState([]);

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        let data = await listSetupData('honey_kind');
        setHoneyKinds(data);
        setPageStatus('Ok');
      } catch (error) {
        setPageStatus(dealWithError(error));
      }
    };

    fetchData();
  }, [honeyKinds, setHoneyKinds, setPageStatus])


  const postData = async (data) => {
    try {
      await createApiary(data);
      props.history.push('/manage/apiary');
    } catch (error) {
      dealWithError(error);
    }
  }

  let genericPage = getGenericPage(pageStatus);
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
          <Divider style={{ paddingLeft: '20px' }} plain />
          <br />
        </Col>
      </Row>
      <Row>
        <Col span={8}>
          <Form {...formItemLayout} onFinish={postData} requiredMark={false}>
            <Form.Item label={window.i18n("word.name")} name="name" rules={[{ required: true, message: window.i18n('form.insertApiaryName') }]}>
              <Input />
            </Form.Item>
            <Form.Item label={window.i18n("word.location")} name="location" rules={[{ required: true, message: window.i18n('form.insertApiaryLocation') }]}>
              <Input />
            </Form.Item>
            <Form.Item label={window.i18n("word.honeyKind")} name="honey_kind" rules={[{ required: true, message: window.i18n('form.selectApiaryHoneyType') }]}>
              <Select defaultValue={window.i18n('form.selectAValue')}>
                {
                  honeyKinds.map(data => {
                    return (
                      <Select.Option key={data.value}>{data.value}</Select.Option>
                    )
                  })
                }
              </Select>
            </Form.Item>
            <Form.Item {...tailFormItemLayout}>
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
