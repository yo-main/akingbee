import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select, Divider, Card } from 'antd';
import { navigate } from '@reach/router';

import { OptionalFormItem, FormLinkModal } from '../../components';
import { dealWithError, notificate } from '../../lib/common';
import { formItemLayout, tailFormItemLayout } from '../../constants';

import { getSetupData } from '../../services/aristaeus/setup';
import { getApiaries } from '../../services/aristaeus/apiary';
import { createHive, getHives, updateHive, deleteHive, getHive } from '../../services/aristaeus/hive';

import { NOT_FOUND_STATUS, ERROR_STATUS, LOADING_STATUS, getGenericPage } from '../generic';

export function UpdateHiveForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "hiveId": props.hive.id,
    "name": props.hive.name,
    "owner": props.hive.ownerId,
    "condition": props.hive.conditionId,
  })

  return (
    <Form {... formItemLayout} id="updateHiveFormId" form={form} name="basic" onFinish={props.onFinish}>
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
  state = {tableData: [], hiveBeekeeper: [], hiveCondition: [], pageStatus: LOADING_STATUS}

  getTableData = (data) => {
    return data.reduce((acc, val, index) => {
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
  }

  async componentDidMount() {
    try {
      let hives = await getHives();
      let hiveBeekeeper = await getSetupData('hive_beekeeper');
      let hiveCondition = await getSetupData('hive_condition');
      let tableData = this.getTableData(hives);
      let pageStatus = 'OK';

      this.setState({hives, hiveBeekeeper, hiveCondition, pageStatus, tableData});

    } catch (error) {
      dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = ERROR_STATUS;
      })
    }
  }

  deleteData = async(hiveId) => {
    try {
      await deleteHive(hiveId);
      let hives = await getHives();
      let tableData = this.getTableData(hives);

      this.setState((state) => {
        state['hives'] = hives;
        state['tableData'] = tableData;
        return state;
      })
    } catch (error) {
      dealWithError(error);
      return
    };


  }

  updateData = async(form) => {
    const hiveId = form.hiveId;
    const data = {
      name: form.name,
      owner_id: form.owner,
      condition_id: form.condition
    }

    try {
      await updateHive(hiveId, data);

      let hives = await getHives();
      let tableData = this.getTableData(hives);
      this.setState((state) => {
        state['hives'] = hives;
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
        render: (text, record) => {
          let url = `${window.location.pathname}/${record.id}`
          return <a href={url}>{text}</a>;
        }
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
              <UpdateHiveForm hive={record} owners={this.state.hiveBeekeeper} conditions={this.state.hiveCondition} onFinish={this.updateData} />
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
    pageStatus: LOADING_STATUS,
    hiveBeekeeper: [],
    hiveCondition: [],
    apiaries: [],
    swarmHealthStatus: [],
  }

  async componentDidMount() {
    try {
      let hiveBeekeeper = await getSetupData('hive_beekeeper');
      let hiveCondition = await getSetupData('hive_condition');
      let swarmHealthStatus = await getSetupData('swarm_health_status');
      let apiaries = await getApiaries();
      let pageStatus = "OK";

      this.setState({apiaries, hiveBeekeeper, hiveCondition, swarmHealthStatus, pageStatus});
    } catch (error) {
      dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = ERROR_STATUS;
      })
    }
  }

  async postData(data) {
    try {
      await createHive(data);
      navigate('/manage/hive');
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
              beekeepers={this.state['hiveBeekeeper']}
              conditions={this.state['hiveCondition']}
              swarmHealths={this.state['swarmHealthStatus']}
              apiaries={this.state['apiaries']}
            />
          </Col>
        </Row>
      </>
    )
  }
}

export class HiveDetailsPage extends React.Component {
  state = {
    pageStatus: LOADING_STATUS,
    hive: [],
    hiveBeekeeper: [],
    hiveCondition: [],
    apiaries: [],
    swarmHealthStatus: [],
  }

  async componentDidMount() {
    let hive;

    try {
      hive = await getHive(this.props.hiveId);
    } catch (error) {
      this.setState((state) => {
        state['pageStatus'] = NOT_FOUND_STATUS;
        return state;
      })
      return;
    }

    try {
      let apiaries = await getApiaries('apiaries');
      let hiveBeekeeper = await getSetupData('hive_beekeeper');
      let hiveCondition = await getSetupData('hive_condition');
      let swarmHealthStatus = await getSetupData('swarm_health_status');
      let pageStatus = "OK"
      this.setState({hive, apiaries, hiveBeekeeper, hiveCondition, swarmHealthStatus, pageStatus});

    } catch (error) {
      dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = ERROR_STATUS;
      })
    }
  }

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };
    console.log(this.state)

    return (
      <p>POPOPO</p>
    )
  }

}