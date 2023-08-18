import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select, Divider, Card, Tabs } from 'antd';
import Icon from '@ant-design/icons';
import { Link } from 'react-router-dom';

import { OptionalFormItem, FormLinkModal, CascaderForm } from '../../components';
import { dealWithError, notificate } from '../../lib/common';
import { formItemLayout, tailFormItemLayout } from '../../constants';

import { ReactComponent as queenSVG } from '../../images/queen.svg';

import { listSetupData } from '../../services/aristaeus/setup';
import { getApiaries } from '../../services/aristaeus/apiary';
import { createHive, getHives, updateHive, removeApiary, deleteHive, getHive, moveHive } from '../../services/aristaeus/hive';
import { deleteSwarm, createSwarm, updateSwarm } from '../../services/aristaeus/swarm';

import { LOADING_STATUS, getGenericPage } from '../generic';

import { CommentTableComponent } from '../../components/commentTable';
import { EventTableComponent } from '../../components/eventTable';

import '../styles.css';


const QUEEN_INVISIBLE = "#FFFFFF";
const QUEEN_BLUE = "#01A0FF";
const QUEEN_WHITE = "#CECFCD";
const QUEEN_YELLOW = "#E2D70F";
const QUEEN_RED = "#E24739";
const QUEEN_GREEN = "#50C375";

const QUEEN_COLOR_MAPPING = {
  0: QUEEN_BLUE,
  1: QUEEN_WHITE,
  2: QUEEN_YELLOW,
  3: QUEEN_RED,
  4: QUEEN_GREEN,
}


function onFailed(err) {
  notificate("error", "Failed")
}

export function UpdateHiveForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "hiveId": props.hive.public_id,
    "name": props.hive.name,
    "owner": props.hive.owner,
    "condition": props.hive.condition,
  })

  let swarmMenuItems = <></>;
  if (props.hive.swarm) {
    form.setFieldsValue({
      "swarmId": props.hive.swarm.public_id,
      "health": props.hive.swarm.health,
      "queenYear": props.hive.swarm.queen_year,
    })

    swarmMenuItems = (
      <>
        <Form.Item label={window.i18n("word.swarmHealth")} name="health">
          <Select>
            {
              props.healths.map(data => {
                return (
                  <Select.Option key={data.value}>{data.value}</Select.Option>
                )
              })
            }
          </Select>
        </Form.Item>
        <Form.Item label={window.i18n("word.queenYear")} name="queenYear" rules={[{ required: true, message: window.i18n('form.insertQueenYear') }]}>
          <Input type="number" />
        </Form.Item>
        <Form.Item name="swarmId" hidden={true} />
      </>
    )
  }

  return (
    <Form {...formItemLayout} id={props.formId} form={form} onFinish={props.onFinish} onFailed={onFailed} requiredMark={false}>
      <Form.Item label={window.i18n("word.name")} name="name" rules={[{ required: true, type: 'string', min: 1, message: window.i18n('form.insertHiveName') }]}>
        <Input />
      </Form.Item>
      <Form.Item label={window.i18n("word.owner")} name="owner">
        <Select>
          {
            props.owners.map(data => {
              return (
                <Select.Option key={data.value}>{data.value}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item label={window.i18n("form.hiveCondition")} name="condition">
        <Select>
          {
            props.conditions.map(data => {
              return (
                <Select.Option key={data.value}>{data.value}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      {swarmMenuItems}
      <Form.Item name="hiveId" hidden={true} />
    </Form>
  )
}

function CreateHiveForm(props) {
  return (
    <Form {...formItemLayout} onFinish={props.callback} onFailed={onFailed} requiredMark={false}>
      <Form.Item label={window.i18n("word.name")} name="name" rules={[{ required: true, message: window.i18n('form.insertHiveName') }]}>
        <Input />
      </Form.Item>
      <Form.Item label={window.i18n("word.owner")} name="owner" rules={[{ required: true, message: window.i18n('form.insertHiveOwner') }]}>
        <Select placeholder={window.i18n('form.selectAValue')}>
          {
            props.owners.map(data => {
              return (
                <Select.Option key={data.value}>{data.value}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item label={window.i18n("word.condition")} name="condition" rules={[{ required: true, message: window.i18n('form.selectHiveCondition') }]}>
        <Select placeholder={window.i18n('form.selectAValue')}>
          {
            props.conditions.map(data => {
              return (
                <Select.Option key={data.value}>{data.value}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <OptionalFormItem buttonName={window.i18n("form.addToApiary")} label={window.i18n("word.apiary")} name="apiary_id" rules={[{ required: true, message: window.i18n('form.selectHiveApiary') }]}>
        <Select placeholder={window.i18n('form.selectAValue')}>
          {
            props.apiaries.map(data => {
              return (
                <Select.Option key={data.public_id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </OptionalFormItem>
      <OptionalFormItem buttonName={window.i18n("form.addSwarm")} label={window.i18n("word.swarmHealth")} name="swarm_health" rules={[{ required: true, message: window.i18n('form.selectSwarmHealth') }]}>
        <Select placeholder={window.i18n('form.selectAValue')}>
          {
            props.swarmHealths.map(data => {
              return (
                <Select.Option key={data.value}>{data.value}</Select.Option>
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
  state = { tableData: [], hiveBeekeeper: [], hiveCondition: [], swarmHealths: [], pageStatus: LOADING_STATUS }

  getTableData = (data) => {
    return data.reduce((acc, val, index) => {
      acc.push({
        key: index + 1,
        public_id: val.public_id,
        name: val.name,
        owner: val.owner,
        condition: val.condition,
        swarm: val.swarm,
        apiary: val.apiary,
      });
      return acc;
    }, []);
  }

  async componentDidMount() {
    try {
      let promises = [
        getHives(true),
        listSetupData('owner'),
        listSetupData('hive_condition'),
        listSetupData('swarm_health')
      ];

      let data = await Promise.all(promises);

      let tableData = this.getTableData(data[0]);
      let pageStatus = 'OK';

      this.setState({ hives: data[0], hiveBeekeeper: data[1], hiveCondition: data[2], swarmHealths: data[3], pageStatus, tableData });

    } catch (error) {
      let status = dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = status;
        return state;
      })
    }
  }

  deleteData = async (hiveId) => {
    try {
      await deleteHive(hiveId);
      let hives = await getHives(true);
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

  updateData = async (form) => {
    const hiveId = form.hiveId;
    const swarmId = form.swarmId;
    const hiveData = {
      name: form.name,
      owner: form.owner,
      condition: form.condition
    }
    const swarmData = {
      health: form.health,
      queen_year: form.queenYear
    }

    try {
      await updateHive(hiveId, hiveData);
      if (swarmId) {
        await updateSwarm(swarmId, swarmData);
      }

      let hives = await getHives(true);
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
          let url = `${window.location.pathname}/${record.public_id}`
          return <Link to={url}>{text}</Link>;
        }
      },
      {
        title: window.i18n('word.apiary'),
        dataIndex: ['apiary', 'name']
      },
      {
        title: window.i18n('word.owner'),
        dataIndex: 'owner',
      },
      {
        title: window.i18n('word.condition'),
        dataIndex: 'condition'
      },
      {
        title: window.i18n('word.swarmHealth'),
        dataIndex: ['swarm', 'health']
      },
      {
        title: window.i18n('word.queenYear'),
        dataIndex: ['swarm', 'queen_year'],
        render: (text, record) => {
          if (record.swarm === null || record.swarm.queen_year === 1900) {
            return "";
          }
          let queenColor = QUEEN_COLOR_MAPPING[record.swarm.queen_year % 5];
          return <>{text} &nbsp;&nbsp;&nbsp;<span style={{ fontSize: 20, color: queenColor }}>■</span></>;
        }
      },
      {
        title: window.i18n('word.actions'),
        key: 'action',
        render: (text, record) => {
          let formId = `updateHive${record.key}`;
          return (
            <Space size='middle'>
              <FormLinkModal formId={formId} title={window.i18n('title.hiveUpdate')} linkContent={window.i18n('word.edit')}>
                <UpdateHiveForm formId={formId} hive={record} owners={this.state.hiveBeekeeper} conditions={this.state.hiveCondition} healths={this.state.swarmHealths} onFinish={this.updateData} />
              </FormLinkModal>
              <Popconfirm onConfirm={() => this.deleteData(record.public_id)} title={window.i18n("confirm.deleteHive")}>
                <Button type="link">{window.i18n('word.delete')}</Button>
              </Popconfirm>
            </Space>
          )
        }
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


export class HiveStockPage extends React.Component {
  state = { hives: [], tableData: [], hiveBeekeeper: [], hiveCondition: [], pageStatus: LOADING_STATUS }

  getTableData = (data) => {
    return data.reduce((acc, val, index) => {
      acc.push({
        key: index + 1,
        public_id: val.public_id,
        name: val.name,
        owner: val.owner,
        condition: val.condition,
      });
      return acc;
    }, []);
  }

  async componentDidMount() {
    try {
      let promises = [
        getHives(false),
        listSetupData('owner'),
        listSetupData('hive_condition')
      ];

      let data = await Promise.all(promises);

      let tableData = this.getTableData(data[0]);
      let pageStatus = 'OK';

      this.setState({ hives: data[0], hiveBeekeeper: data[1], hiveCondition: data[2], pageStatus, tableData });

    } catch (error) {
      let status = dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = status;
        return state;
      })
    }
  }

  deleteData = async (hiveId) => {
    try {
      await deleteHive(hiveId);
      let hives = await getHives(false);
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

  updateData = async (form) => {
    const hiveId = form.hiveId;
    const hiveData = {
      name: form.name,
      owner: form.owner,
      condition: form.condition
    }

    try {
      await updateHive(hiveId, hiveData);

      let hives = await getHives(false);
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
          let url = `/manage/hive/${record.public_id}`
          return <Link to={url}>{text}</Link>;
        }
      },
      {
        title: window.i18n('word.owner'),
        dataIndex: 'owner',
      },
      {
        title: window.i18n('word.condition'),
        dataIndex: 'condition'
      },
      {
        title: window.i18n('word.actions'),
        key: 'action',
        render: (text, record) => {
          let formId = `updateHive${record.key}`;
          return (
            <Space size='middle'>
              <FormLinkModal formId={formId} title={window.i18n('title.hiveUpdate')} linkContent={window.i18n('word.edit')}>
                <UpdateHiveForm formId={formId} hive={record} owners={this.state.hiveBeekeeper} conditions={this.state.hiveCondition} onFinish={this.updateData} />
              </FormLinkModal>
              <Popconfirm onConfirm={() => this.deleteData(record.public_id)} title={window.i18n("confirm.deleteHive")}>
                <Button type="link">{window.i18n('word.delete')}</Button>
              </Popconfirm>
            </Space>
          )
        }
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
      let promises = [
        listSetupData('owner'),
        listSetupData('hive_condition'),
        listSetupData('swarm_health'),
        getApiaries(),
      ];
      let data = await Promise.all(promises);

      let pageStatus = "OK";

      this.setState({ apiaries: data[3], owners: data[0], hiveConditions: data[1], swarmHealths: data[3], pageStatus });
    } catch (error) {
      let status = dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = status;
      })
    }
  }

  postData = async (data) => {
    try {
      await createHive(data);
      if (data.apiary_id === undefined) {
        this.props.history.push('/manage/hive/stock');
      } else {
        this.props.history.push('/manage/hive');
      }

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
            <Divider style={{ paddingLeft: '20px' }} plain />
            <br />
          </Col>
        </Row>
        <Row>
          <Col span={8}>
            <CreateHiveForm
              callback={this.postData}
              owners={this.state['owners']}
              conditions={this.state['hiveConditions']}
              swarmHealths={this.state['swarmHealths']}
              apiaries={this.state['apiaries']}
            />
          </Col>
        </Row>
      </>
    )
  }
}

export class HiveDetailsPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pageStatus: LOADING_STATUS,
      hive: {},
      hiveBeekeeper: [],
      hiveCondition: [],
      apiaries: [],
      swarmHealthStatus: [],
    }
  }

  updateHiveData = async (form) => {
    const hiveId = form.hiveId;
    const swarmId = form.swarmId;
    const hiveData = {
      name: form.name,
      owner: form.owner,
      condition: form.condition
    }
    const swarmData = {
      health: form.health,
      queen_year: form.queenYear
    }

    try {
      await updateHive(hiveId, hiveData);
      if (swarmId) {
        await updateSwarm(swarmId, swarmData);
      }

      let hive = await getHive(hiveId);
      this.setState((state) => {
        state['hive'] = hive;
        return state;
      })
    } catch (error) {
      dealWithError(error);
    }
  }

  async componentDidMount() {
    let hive;

    let { hiveId } = this.props.match.params;

    try {
      hive = await getHive(hiveId);
    } catch (error) {
      let status = dealWithError(error);

      this.setState((state) => {
        state['pageStatus'] = status;
        return state;
      })

      return;
    }

    try {
      let promises = [
        getApiaries(),
        listSetupData('owner'),
        listSetupData('hive_condition'),
        listSetupData('swarm_health')
      ];

      let data = await Promise.all(promises);

      let pageStatus = "OK"
      this.setState({ hive, apiaries: data[0], hiveBeekeeper: data[1], hiveCondition: data[2], swarmHealthStatus: data[3], pageStatus });

    } catch (error) {
      let status = dealWithError(error);

      this.setState((state) => {
        state['pageStatus'] = status;
        return state;
      })
    }
  }

  getCascaderOptions = () => {
    let options = [];

    let current_apiary = this.state.hive.apiary;
    let apiaries = this.state.apiaries;
    let health_statuses = this.state.swarmHealthStatus;

    if (this.state.hive.apiary) {
      options.push({
        label: window.i18n('form.removeApiary'),
        value: "removeApiary"
      });
    }

    let apiaryConfig = {
      label: window.i18n('form.moveHive'),
      value: "newApiary",
      children: apiaries.reduce((acc, val) => {
        if (!current_apiary || current_apiary.public_id !== val.public_id) {
          acc.push({
            value: val.public_id,
            label: val.name,
          });
        }
        return acc;
      }, [{
        value: window.i18n("word.name"),
        label: window.i18n("word.name"),
        disabled: true
      }])
    };

    if (apiaryConfig.children.length > 0) {
      options.push(apiaryConfig);
    }

    if (this.state.hive.swarm) {
      options.push({
        label: window.i18n('form.deleteSwarm'),
        value: "deleteSwarm"
      })
    } else {
      options.push({
        label: window.i18n('form.addSwarm'),
        value: "addSwarm",
        children: health_statuses.reduce((acc, val) => {
          acc.push({
            value: val.value,
            label: val.value,
          });
          return acc;
        }, [{
          value: window.i18n("word.health"),
          label: window.i18n("word.health"),
          disabled: true
        }])
      })
    }


    options.push({
      label: window.i18n('form.deleteHive'),
      value: "deleteHive"
    })

    return options
  }

  onCascaderSubmit = async ({ action }) => {
    if (action === undefined) {
      return;
    }

    switch (action[0]) {
      case 'newApiary':
        let apiary_id = action[1];
        try {
          await moveHive(this.state.hive.public_id, apiary_id);
          let hive = await getHive(this.state.hive.public_id)
          this.setState((state) => {
            state['hive'] = hive;
            return state;
          })
          notificate('success', window.i18n('form.hiveMovedSuccess'))
        } catch (error) {
          dealWithError(error);
        }
        break;
      case 'removeApiary':
        try {
          await removeApiary(this.state.hive.public_id);
          let hive = await getHive(this.state.hive.public_id)
          this.setState((state) => {
            state['hive'] = hive;
            return state;
          })
          notificate('success', window.i18n('form.hiveApiaryRemovedSuccess'))
        } catch (error) {
          dealWithError(error);
        }
        break;
      case 'deleteHive':
        try {
          await deleteHive(this.state.hive.public_id);
          notificate('success', window.i18n('form.hiveDeletedSuccess'));
          this.props.history.push("/manage/hive");
        } catch (error) {
          dealWithError(error);
        }
        break;
      case 'deleteSwarm':
        try {
          await deleteSwarm({ swarm_id: this.state.hive.swarm.public_id });
          let hive = await getHive(this.state.hive.public_id)
          this.setState((state) => {
            state['hive'] = hive;
            return state;
          })
          notificate('success', window.i18n('form.swarmDeletedSuccess'))
        } catch (error) {
          dealWithError(error);
        }
        break;
      case 'addSwarm':
        try {
          let swarm = await createSwarm({ health: action[1], queen_year: new Date().getFullYear() });
          let hive = await updateHive(this.state.hive.public_id, { swarm_id: swarm.public_id })
          this.setState((state) => {
            state['hive'] = hive;
            return state;
          })
          notificate('success', window.i18n('form.swarmAddedSuccess'))
        } catch (error) {
          dealWithError(error);
        }
        break;
      case 'harvest':
        try {
          let swarm = await createSwarm({ health: action[1], queen_year: new Date().getFullYear() });
          let hive = await updateHive(this.state.hive.public_id, { swarm_id: swarm.public_id })
          this.setState((state) => {
            state['hive'] = hive;
            return state;
          })
          notificate('success', window.i18n('form.swarmAddedSuccess'))
        } catch (error) {
          dealWithError(error);
        }
        break;
      default:
        notificate('error', 'Something went wrong with the chosen action - sorry');
    }
  }

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

    const cardItems = (label, value) => {
      return <p> {label} : {value}</p>
    }

    let name = this.state.hive.name;
    let owner = cardItems(window.i18n('word.owner'), this.state.hive.owner);
    let condition = cardItems(window.i18n('form.hiveCondition'), this.state.hive.condition);

    let health, apiary;
    if (this.state.hive.swarm) {
      health = cardItems(window.i18n('word.swarmHealth'), this.state.hive.swarm.health);
    };
    if (this.state.hive.apiary) {
      apiary = cardItems(window.i18n('word.apiary'), this.state.hive.apiary.name);
    };

    let updateHiveForm = (
      <FormLinkModal title={window.i18n('title.hiveUpdate')} formId='updateHiveFormId' linkContent={window.i18n('word.edit')}>
        <UpdateHiveForm
          formId='updateHiveFormId'
          hive={this.state.hive}
          owners={this.state.hiveBeekeeper}
          healths={this.state.swarmHealthStatus}
          conditions={this.state.hiveCondition}
          onFinish={this.updateHiveData}
        />
      </FormLinkModal>
    );

    let cascaderOptions = this.getCascaderOptions();

    let queenColor = QUEEN_INVISIBLE;
    if (this.state.hive.swarm && this.state.hive.swarm.queen_year !== 1900) {
      queenColor = QUEEN_COLOR_MAPPING[this.state.hive.swarm.queen_year % 5];
    }

    return (
      <>
        <Row>
          <Col offset="1">
            <Card title={`${window.i18n("word.info")} ${name}`} size="default" type="inner" extra={<div style={{ paddingLeft: '50px' }}>{updateHiveForm}</div>}>
              <Row>
                <Col span={22}>
                  {owner}
                </Col>
                <Col span={2}>
                  <Icon style={{ fontSize: 35, color: queenColor }} component={queenSVG} />
                </Col>
              </Row>
              {apiary}
              {condition}
              {health}
              {/* {year} */}
            </Card>
          </Col>
          <Col style={{ paddingLeft: '10px' }}>
            <CascaderForm title={window.i18n('form.manageHive')} options={cascaderOptions} onFinish={this.onCascaderSubmit} />
          </Col>
          <Col offset={14}>
          </Col>
        </Row>
        <Col offset="1">
          <Divider />
        </Col>
        <Row>
          <Col offset="1" span="23">
            <div className="card-container">
              <Tabs defaultActiveKey="1" type="card">
                <Tabs.TabPane tab={window.i18n("word.history")} key="1">
                  <CommentTableComponent hiveId={this.state.hive.public_id} />
                </Tabs.TabPane>
                <Tabs.TabPane tab={window.i18n("word.events")} key="2">
                  <EventTableComponent hiveId={this.state.hive.public_id} />
                </Tabs.TabPane>
              </Tabs>
            </div>
          </Col>
        </Row>
      </>
    )
  }
}
