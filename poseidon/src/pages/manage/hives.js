import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select, Divider } from 'antd';

import { OptionalFormItem, FormLinkModal } from '../../components';
import { notificate } from '../../lib/common';
import { formItemLayout, tailFormItemLayout } from '../../constants';

import { getSetupData } from '../../services/aristaeus/setup';
import { getApiaries } from '../../services/aristaeus/apiary';
import { createHive, getHives, updateHive, deleteHive } from '../../services/aristaeus/hive';
import { navigate } from '@reach/router';


function onFailed(err) {
  notificate("error", "Failed")
}

export function UpdateHiveForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "hiveId": props.hive.id,
    "name": props.hive.name,
    "owner": props.hive.ownerId,
    "condition": props.hive.conditionId,
  })

  return (
    <Form {... formItemLayout} id="updateHiveFormId" form={form} name="basic" onFinish={props.onFinish} onFinishFailed={onFailed}>
      <Form.Item label={window.i18n("word.name")} name="name" rules={[{type: 'string', min: 1, message: window.i18n('form.insertHiveName')}]}>
        <Input defaultValue={props.hive.name} />
      </Form.Item>
      <Form.Item label={window.i18n("word.owner")} name="owner" rules={[{message: window.i18n('form.selectHiveOwner')}]}>
        <Select defaultValue={props.hive.ownerId}>
          {
            props.owners.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item label={window.i18n("word.condition")} name="condition" rules={[{message: window.i18n('form.selectHiveCondition')}]}>
        <Select defaultValue={props.hive.conditionId}>
          {
            props.conditions.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item name="hiveId" hidden={true} />
    </Form>
  )
}

function CreateHiveForm(props) {
  return (
    <Form {...formItemLayout} onFinish={props.callback} requiredMark={false}>
      <Form.Item label={window.i18n("word.name")} name="name" rules={[{required: true, message: window.i18n('form.insertHiveName')}]}>
        <Input />
      </Form.Item>
      <Form.Item label={window.i18n("word.owner")} name="owner_id" rules={[{required: true, message: window.i18n('form.insertHiveOwner')}]}>
        <Select defaultValue={window.i18n('form.selectAValue')}>
          {
            props.beekeepers.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item label={window.i18n("word.condition")} name="condition_id" rules={[{required: true, message: window.i18n('form.selectHiveCondition')}]}>
        <Select defaultValue={window.i18n('form.selectAValue')}>
          {
            props.conditions.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <OptionalFormItem buttonName={window.i18n("form.addToApiary")} label={window.i18n("word.apiary")} name="apiary_id" rules={[{required: true, message: window.i18n('form.selectHiveApiary')}]}>
        <Select defaultValue={window.i18n('form.selectAValue')}>
          {
            props.apiaries.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </OptionalFormItem>
      <OptionalFormItem buttonName={window.i18n("form.addSwarm")} label={window.i18n("word.swarmHealth")} name="swarm_health_id" rules={[{required: true, message: window.i18n('form.selectSwarmHealth')}]}>
        <Select defaultValue={window.i18n('form.selectAValue')}>
          {
            props.swarmHealths.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </OptionalFormItem>
      <Form.Item {...tailFormItemLayout}>
        <Button type="primary" htmlType="submit">
          {window.i18n('word.submit')}
        </Button>
      </Form.Item>
    </Form>
  )
}


export class HivePage extends React.Component {
  state = {tableData: [], hive_beekeeper: [], hive_condition: []}

  refreshTableContent = ({data}) => {
    const tableData = data.reduce((acc, val, index) => {
        acc.push({
          key: index+1,
          id: val.id,
          name: val.name,
          owner: val.owner.name,
          ownerId: val.owner.id,
          condition: val.condition.name,
          conditionId: val.condition.id,
          swarmHealthStatus: val.swarm ? val.swarm.health.name : null,
          swarmHealthStatusId: val.swarm ? val.swarm.health.id : null,
          apiary: val.apiary ? val.apiary.name : null,
          apiaryId: val.apiary ? val.apiary.id : null,
        });
        return acc;
      }, []);

    this.setState((state) => {
      state.tableData = tableData;
      return state;
    });
  }

  refreshState = ({data, type}) => {
    this.setState((state) => {
      state[type] = data;
      return state;
    })
  }

  componentDidMount() {
    getHives(this.refreshTableContent);
    getSetupData(this.refreshState, 'hive_beekeeper');
    getSetupData(this.refreshState, 'hive_condition');
  }

  deleteData = (hiveId) => {
    deleteHive(hiveId, () => getHives(this.refreshTableContent));
  }

  updateData = (form) => {
    const hiveId = form.hiveId
    const data = {
      name: form.name,
      owner_id: form.owner,
      condition_id: form.condition
    }
    updateHive(hiveId, data, () => getHives(this.refreshTableContent));
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
        title: window.i18n('word.owner'),
        dataIndex: 'owner',
        key: 'owner',
      },
      {
        title: window.i18n('word.condition'),
        dataIndex: 'condition',
        key: 'condition',
      },
      {
        title: window.i18n('word.swarmHealth'),
        dataIndex: 'swarmHealthStatus',
        key: 'swarmHealthStatus',
      },
      {
        title: window.i18n('word.apiary'),
        dataIndex: 'apiary',
        key: 'apiary',
      },
      {
        title: window.i18n('word.actions'),
        key: 'action',
        render: (text, record) => (
          <Space size='middle'>
            <FormLinkModal title={window.i18n('title.hiveUpdate')} formId='updateHiveFormId' linkContent={window.i18n('word.edit')}>
              <UpdateHiveForm hive={record} owners={this.state.hive_beekeeper} conditions={this.state.hive_condition} onFinish={this.updateData} />
            </FormLinkModal>
            <Popconfirm onConfirm={() => this.deleteData(record.id)} title={window.i18n("confirm.deleteHive")}>
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



export class HiveCreationPage extends React.Component {
  state = {
    hive_beekeeper: [],
    hive_condition: [],
    apiaries: [],
    swarm_health_status: [],
  }

  refreshState = ({data, type}) => {
    this.setState((state) => {
      state[type] = data;
      return state;
    })
  }

  componentDidMount() {
    getSetupData(this.refreshState, 'hive_beekeeper');
    getSetupData(this.refreshState, 'hive_condition');
    getSetupData(this.refreshState, 'swarm_health_status');
    getApiaries(this.refreshState, 'apiaries');
  }

  postData(data) {
    createHive(data, () => navigate('/manage/hive'));
  }

  render() {
    return (
      <>
        <Row>
          <Col offset={1}>
            <h1>{window.i18n('title.hiveCreation')}</h1>
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
            <CreateHiveForm
              callback={this.postData}
              beekeepers={this.state['hive_beekeeper']}
              conditions={this.state['hive_condition']}
              swarmHealths={this.state['swarm_health_status']}
              apiaries={this.state['apiaries']}
            />
          </Col>
        </Row>
      </>
    )
  }
}

export class HiveDetailsPage {

}