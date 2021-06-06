import React from 'react';

import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select, Divider, Card, Tabs, DatePicker } from 'antd';
import { navigate, Link } from '@reach/router';

import { OptionalFormItem, FormLinkModal, FormButtonModal, CascaderForm, RichEditor, EditorReadOnly } from '../../components';
import { dealWithError, notificate } from '../../lib/common';
import { formItemLayout, tailFormItemLayout } from '../../constants';

import { getSetupData } from '../../services/aristaeus/setup';
import { getApiaries } from '../../services/aristaeus/apiary';
import { getCommentsForHive, postCommentForHive, putComment, deleteComment } from '../../services/aristaeus/comments';
import { getEvents, postEvent, putEvent, deleteEvent } from '../../services/aristaeus/events';
import { createHive, getHives, updateHive, deleteHive, getHive, moveHive } from '../../services/aristaeus/hive';
import { deleteSwarm, createSwarm } from '../../services/aristaeus/swarm';

import { NOT_FOUND_STATUS, ERROR_STATUS, LOADING_STATUS, getGenericPage } from '../generic';

import '../styles.css';
import { PlusOutlined } from '@ant-design/icons';

import moment from 'moment';

function onFailed(err) {
  notificate("error", "Failed")
}

export function UpdateHiveForm(props) {
  const [form] = Form.useForm();

  form.setFieldsValue({
    "hiveId": props.hive.id,
    "name": props.hive.name,
    "owner": props.hive.owner.id,
    "condition": props.hive.condition.id,
  })

  return (
    <Form {... formItemLayout} id={props.formId} form={form} name="basic" onFinish={props.onFinish} onFailed={onFailed}>
      <Form.Item label={window.i18n("word.name")} name="name" rules={[{type: 'string', min: 1, message: window.i18n('form.insertHiveName')}]}>
        <Input defaultValue={props.hive.name} />
      </Form.Item>
      <Form.Item label={window.i18n("word.owner")} name="owner" rules={[{message: window.i18n('form.selectHiveOwner')}]}>
        <Select defaultValue={props.hive.owner.id}>
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
        <Select defaultValue={props.hive.condition.id}>
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
    <Form {...formItemLayout} onFinish={props.callback} onFailed={onFailed} requiredMark={false}>
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

function CreateCommentForm(props) {
  const [form] = Form.useForm();

  const onChange = (data) => {
    form.setFieldsValue({comment: data })
  }

  const onFinish = (data) => {
    props.onFinish(data);
    form.resetFields();
  }

  return (
    <Form id="newComment" form={form} layout="vertical" requiredMark={false} onFinish={onFinish} onFailed={onFailed}>
      <Form.Item label={window.i18n("word.date")} name="date">
        <DatePicker />
      </Form.Item>
      <Form.Item label={window.i18n("word.comment")} name="comment">
        <RichEditor onChange={onChange} />
      </Form.Item>
    </Form>
  )
}

function CreateEventForm(props) {
  const [form] = Form.useForm();

  const onChange = (data) => {
    form.setFieldsValue({description: data })
  }

  const onFinish = (data) => {
    props.onFinish(data);
    form.resetFields();
  }

  return (
    <Form id="newEvent" form={form} layout="vertical" requiredMark={false} onFinish={onFinish} onFailed={onFailed}>
      <Form.Item label={window.i18n("word.dueDate")} name="dueDate">
        <DatePicker />
      </Form.Item>
      <Form.Item label={window.i18n("word.title")} name="title">
        <Input />
      </Form.Item>
      <Form.Item label={window.i18n("word.type")} name="typeId" rules={[{required: true, message: window.i18n('form.type')}]}>
        <Select defaultValue={window.i18n('form.selectAValue')}>
          {
            props.eventTypes.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item label={window.i18n("word.status")} name="statusId" rules={[{required: true, message: window.i18n('form.status')}]}>
        <Select defaultValue={window.i18n('form.selectAValue')}>
          {
            props.eventStatuses.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item label={window.i18n("word.description")} name="description">
        <RichEditor onChange={onChange} />
      </Form.Item>
    </Form>
  )
}



function UpdateEventForm(props) {
  const [form] = Form.useForm();
  form.setFieldsValue({
    "eventId": props.eventId,
    "dueDate": props.dueDate,
    "title": props.title,
    "description": props.description,
    "statusId": props.status.id
  });

  const onChange = (data) => {
    form.setFieldsValue({description: data })
  };

  return (
    <Form id={props.formId} form={form} layout="vertical" requiredMark={false} onFinish={props.onFinish} onFailed={onFailed}>
      <Form.Item label={window.i18n("word.date")} name="dueDate">
        <DatePicker format="L" />
      </Form.Item>
          <Form.Item label={window.i18n("word.title")} name="title">
        <Input />
      </Form.Item>
      <Form.Item label={window.i18n("word.status")} name="statusId" rules={[{required: true, message: window.i18n('form.status')}]}>
        <Select defaultValue={window.i18n('form.selectAValue')}>
          {
            props.eventStatuses.map(data => {
              return (
                <Select.Option key={data.id}>{data.name}</Select.Option>
              )
            })
          }
        </Select>
      </Form.Item>
      <Form.Item label={window.i18n("word.description")} name="description">
        <RichEditor defaultContent={props.description} onChange={onChange} />
      </Form.Item>
      <Form.Item name="eventId" hidden/>
    </Form>
  )
}

function UpdateCommentForm(props) {
  const [form] = Form.useForm();
  form.setFieldsValue({
    "commentId": props.commentId,
    "date": props.date,
    "comment": props.content
  });

  const onChange = (data) => {
    form.setFieldsValue({comment: data })
  };

  return (
    <Form id={props.formId} form={form} layout="vertical" requiredMark={false} onFinish={props.onFinish} onFailed={onFailed}>
      <Form.Item label={window.i18n("word.date")} name="date">
        <DatePicker format="L" />
      </Form.Item>
      <Form.Item label={window.i18n("word.comment")} name="comment">
        <RichEditor defaultContent={props.content} onChange={onChange} />
      </Form.Item>
      <Form.Item name="commentId" hidden/>
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
        return state;
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
    console.log(process.env.REACT_APP_ARISTAEUS_API)
    console.log(process.env.REACT_APP_CERBES_API)


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
          return <Link to={url}>{text}</Link>;
        }
      },
      {
        title: window.i18n('word.owner'),
        dataIndex: ['owner', 'name'],
      },
      {
        title: window.i18n('word.condition'),
        dataIndex: ['condition', 'name']
      },
      {
        title: window.i18n('word.swarmHealth'),
        dataIndex: ['swarm', 'health', 'name']
      },
      {
        title: window.i18n('word.apiary'),
        dataIndex: ['apiary', 'name']
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
              <Popconfirm onConfirm={() => this.deleteData(record.id)} title={window.i18n("confirm.deleteHive")}>
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
  constructor(props) {
    super(props);
    this.state = {
      pageStatus: LOADING_STATUS,
      hive: {},
      hiveBeekeeper: [],
      hiveCondition: [],
      apiaries: [],
      swarmHealthStatus: [],
      commentsTableData: [],
      eventTypes: [],
      eventStatuses: [],
      eventsTableData: [],
    }

    this.refCascader = React.createRef();
  }

  updateHiveData = async(form) => {
    const hiveId = form.hiveId;
    const data = {
      name: form.name,
      owner_id: form.owner,
      condition_id: form.condition
    }

    try {
      await updateHive(hiveId, data);

      let hive = await getHive(hiveId);
      this.setState((state) => {
        state['hive'] = hive;
        return state;
      })
    } catch (error) {
      dealWithError(error);
    }
  }

  getCommentsTableData = (data) => {
    return data.reduce((acc, val, index) => {
      acc.push({
        key: index+1,
        id: val.id,
        comment: val.comment,
        date: val.date,
        type: val.type,
        event: val.event
      });
      return acc;
    }, []);
  }

  getEventsTableData = (data) => {
    return data.reduce((acc, val, index) => {
      acc.push({
        key: index+1,
        id: val.id,
        title: val.title,
        description: val.description,
        dueDate: val.due_date,
        type: val.type,
        status: val.status,
      });
      return acc;
    }, []);
  }


  async componentDidMount() {
    let hive;

    try {
      hive = await getHive(this.props.hiveId);
    } catch (error) {
      if (error.response.status === 404) {
        this.setState((state) => {
          state['pageStatus'] = NOT_FOUND_STATUS;
          return state;
        })
      } else {
        dealWithError(error);
      }

      return;
    }

    try {
      let apiaries = await getApiaries('apiaries');
      let hiveBeekeeper = await getSetupData('hive_beekeeper');
      let hiveCondition = await getSetupData('hive_condition');
      let swarmHealthStatus = await getSetupData('swarm_health_status');
      let eventTypes = await getSetupData('event_type');
      let eventStatuses = await getSetupData('event_status');
      let comments = await getCommentsForHive(this.props.hiveId);
      let events = await getEvents(this.props.hiveId);
      console.log(events);

      let commentsTableData = this.getCommentsTableData(comments);
      let eventsTableData = this.getEventsTableData(events);

      let pageStatus = "OK"
      this.setState({hive, apiaries, hiveBeekeeper, hiveCondition, swarmHealthStatus, commentsTableData, eventsTableData, eventTypes, eventStatuses, pageStatus});

    } catch (error) {
      dealWithError(error);
      this.setState((state) => {
        state['pageStatus'] = ERROR_STATUS;
      });
      this.forceUpdate();
    }
  }

  getCascaderOptions = () => {
    let options = [];

    let current_apiary = this.state.hive.apiary;
    let apiaries = this.state.apiaries;
    let health_statuses = this.state.swarmHealthStatus;

    let apiaryConfig = {
      label: window.i18n('form.moveHive'),
      value: "newApiary",
      children: apiaries.reduce((acc, val) => {
        if (!current_apiary || current_apiary.id !== val.id) {
          acc.push({
            value: val.id,
            label: val.name,
          });
        }
        return acc;
      }, [])
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
            value: val.id,
            label: val.name,
          });
          return acc;
        }, [])
      })
    }

    options.push({
      label: window.i18n('form.deleteHive'),
      value: "deleteHive"
    })

    return options
  }

  onCascaderSubmit = async({action}) => {
    this.refCascader.current.reset();

    if (action === undefined) {
      return;
    }

    switch (action[0]) {
      case 'newApiary':
        let apiary_id = action[1];
        try {
          await moveHive(this.state.hive.id, apiary_id);
          let hive = await getHive(this.state.hive.id)
          this.setState((state) => {
            state['hive'] = hive;
            return state;
          })
          notificate('success', window.i18n('form.hiveMovedSuccess'))
        } catch (error) {
          dealWithError(error);
        }
        break;
      case 'deleteHive':
        try {
          await deleteHive(this.state.hive.id);
          notificate('success', window.i18n('form.hiveDeletedSuccess'));
          navigate("/manage/hive");
        } catch(error) {
          dealWithError(error);
        }
        break;
      case 'deleteSwarm':
        try {
          await deleteSwarm({swarm_id: this.state.hive.swarm.id});
          let hive = await getHive(this.state.hive.id)
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
          let swarm = await createSwarm({health_status_id: action[1]});
          await updateHive(this.state.hive.id, {swarm_id: swarm.id})
          let hive = await getHive(this.state.hive.id)
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

  getCommentsTableColumn() {
    return [
      {
        title: window.i18n('word.date'),
        dataIndex: 'date',
        width: 100,
        defaultSortOrder: 'ascend',
        sorter: (a, b) => a.date.isBefore(b.date),
        render: (text, record) => (
          text.format('L')
        )
      },
      {
        title: window.i18n('word.type'),
        width: 100,
        dataIndex: 'type',
      },
      {
        title: window.i18n('word.comment'),
        dataIndex: 'comment',
        render: (text, record) => {
          return <EditorReadOnly content={JSON.parse(text)} />
        }
      },
      {
        title: window.i18n('word.actions'),
        key: 'action',
        width: 100,
        render: (text, record) => {
          let formId = `updateComment${record.key}`
          return (
            <Space size='middle'>
              <FormLinkModal formId={formId} title={window.i18n('title.editComment')} linkContent={window.i18n('word.edit')}>
                <UpdateCommentForm formId={formId} onFinish={this.updateComment} commentId={record.id} date={record.date} content={JSON.parse(record.comment)} />
              </FormLinkModal>
              <Popconfirm onConfirm={async() => this.deleteComment(record.id)} title={window.i18n("confirm.deleteComment")}>
                <Button type="link">{window.i18n('word.delete')}</Button>
              </Popconfirm>
            </Space>
          )
        }
      }
    ];
  }


  getEventsTableColumn() {
    return [
      {
        title: window.i18n('word.dueDate'),
        dataIndex: 'dueDate',
        width: 100,
        defaultSortOrder: 'ascend',
        sorter: (a, b) => a.dueDate.isBefore(b.dueDate),
        render: (text, record) => (
          text.format('L')
        )
      },
      {
        title: window.i18n('word.type'),
        width: 100,
        dataIndex: ['type', 'name'],
        key: "type",
      },
      {
        title: window.i18n('word.title'),
        dataIndex: 'title',
      },
      {
        title: window.i18n('word.description'),
        dataIndex: 'description',
        render: (text, record) => {
          return <EditorReadOnly content={JSON.parse(text)} />
        }
      },
      {
        title: window.i18n('word.status'),
        dataIndex: ['status', 'name'],
        key: "status",
      },
      {
        title: window.i18n('word.actions'),
        key: 'action',
        width: 100,
        render: (text, record) => {
          let formId = `updateEvent${record.key}`
          return (
            <Space size='middle'>
              <FormLinkModal formId={formId} title={window.i18n('title.editEvent')} linkContent={window.i18n('word.edit')}>
                <UpdateEventForm formId={formId} onFinish={this.updateEvent} eventId={record.id} status={record.status} eventStatuses={this.state.eventStatuses} dueDate={record.dueDate} title={record.title} description={JSON.parse(record.description)} />
              </FormLinkModal>
              <Popconfirm onConfirm={async() => this.deleteEvent(record.id)} title={window.i18n("confirm.deleteEvent")}>
                <Button type="link">{window.i18n('word.delete')}</Button>
              </Popconfirm>
            </Space>
          )
        }
      }
    ];
  }



  deleteComment = async(commentId) => {
    try {
      await deleteComment(commentId);
    } catch (error) {
      dealWithError(error);
      return;
    }

    let comments = await getCommentsForHive(this.props.hiveId);
    let commentsTableData = this.getCommentsTableData(comments);

    this.setState((state) => {
      state['commentsTableData'] = commentsTableData;
      return state;
    });
  }

  deleteEvent = async(eventId) => {
    try {
      await deleteEvent(eventId);
    } catch (error) {
      dealWithError(error);
      return;
    }

    let events = await getEvents(this.props.hiveId);
    let eventsTableData = this.getEventsTableData(events);

    this.setState((state) => {
      state['eventsTableData'] = eventsTableData;
      return state;
    });
  }

  submitComment = async(data) => {
    if (!data.date || !data.comment) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    let date = data.date.toISOString();
    let comment = JSON.stringify(data.comment);

    try {
      await postCommentForHive(this.state.hive.id, {date, comment})
    } catch (error) {
      dealWithError(error);
      return;
    }

    let comments = await getCommentsForHive(this.props.hiveId);
    let commentsTableData = this.getCommentsTableData(comments);

    this.setState((state) => {
      state['commentsTableData'] = commentsTableData;
      return state;
    });
  }

  submitEvent = async(data) => {
    if (!data.dueDate || !data.title || !data.statusId || !data.typeId) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    let dueDate = data.dueDate.toISOString();
    let title = data.title;
    let description = JSON.stringify(data.description);
    let statusId = data.statusId;
    let typeId = data.typeId;
    let hiveId = this.props.hiveId;

    try {
      await postEvent({dueDate, title, description, statusId, typeId, hiveId});
    } catch (error) {
      dealWithError(error);
      return;
    }

    let events = await getEvents(this.props.hiveId);
    let eventsTableData = this.getEventsTableData(events);

    this.setState((state) => {
      state['eventsTableData'] = eventsTableData;
      return state;
    });
  }

  updateComment = async(data) => {
    if (!data.date || !data.comment) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    let commentId = data.commentId;
    let date = data.date.toISOString();
    let comment = JSON.stringify(data.comment);

    try {
      await putComment(commentId, {date, comment})
    } catch (error) {
      dealWithError(error);
      return;
    }

    let comments = await getCommentsForHive(this.props.hiveId);
    let commentsTableData = this.getCommentsTableData(comments);

    this.setState((state) => {
      state['commentsTableData'] = commentsTableData;
      return state;
    });
  }

  updateEvent = async(data) => {
    if (!data.dueDate && !data.title && !data.statusId && !data.description) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    let eventId = data.eventId;
    let dueDate = data.dueDate.toISOString();
    let title = data.title;
    let description = JSON.stringify(data.description);
    let statusId = data.statusId

    try {
      await putEvent(eventId, {dueDate, title, description, statusId})
    } catch (error) {
      dealWithError(error);
      return;
    }

    let events = await getEvents(this.props.hiveId);
    let eventsTableData = this.getEventsTableData(events);

    this.setState((state) => {
      state['eventsTableData'] = eventsTableData;
      return state;
    });
  }


  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

    const cardItems = (label, value) => {
      return <p> {label} : {value}</p>
    }

    let name = this.state.hive.name;
    let owner = cardItems(window.i18n('word.owner'), this.state.hive.owner.name);
    let condition = cardItems(window.i18n('word.condition'), this.state.hive.condition.name);

    let health, apiary;
    if (this.state.hive.swarm) {
      health = cardItems(window.i18n('word.health'), this.state.hive.swarm.health.name);
    };
    if (this.state.hive.apiary) {
      apiary = cardItems(window.i18n('word.apiary'), this.state.hive.apiary.name);
    };

    let updateHiveForm = (
      <FormLinkModal title={window.i18n('title.hiveUpdate')} formId='updateHiveFormId' linkContent={window.i18n('word.edit')}>
        <UpdateHiveForm formId='updateHiveFormId' hive={this.state.hive} owners={this.state.hiveBeekeeper} conditions={this.state.hiveCondition} onFinish={this.updateHiveData} />
      </FormLinkModal>
    );

    let cascaderOptions = this.getCascaderOptions();

    return (
      <>
        <Row>
          <Col offset="1">
            <Card title={`${window.i18n("word.info")} ${name}`} size="default" type="inner" extra={<div style={{paddingLeft: '50px'}}>{updateHiveForm}</div>}>
              {owner}
              {health}
              {apiary}
              {condition}
            </Card>
          </Col>
          <Col style={{paddingLeft: '10px'}}>
            <CascaderForm ref={this.refCascader} title={window.i18n('form.manageHive')} options={cascaderOptions} onFinish={this.onCascaderSubmit}/>
          </Col>
        </Row>
        <Col offset="1">
          <Divider/>
        </Col>
        <Row>
          <Col offset="1" span="23">
            <div className="card-container">
              <Tabs defaultActiveKey="1" type="card">
                <Tabs.TabPane tab={window.i18n("word.history")} key="1">
                  <Row justify="end" style={{marginBottom: '1%'}} >
                    <Col>
                      <FormButtonModal buttonIcon={<PlusOutlined style={{ fontSize: '20px'}}/>} title={window.i18n('title.newComment')} formId='newComment'>
                        <CreateCommentForm onFinish={this.submitComment}/>
                      </FormButtonModal>
                    </Col>
                  </Row>
                  <Row>
                    <Col span="24">
                      <Table dataSource={this.state.commentsTableData} columns={this.getCommentsTableColumn()} pagination={false} bordered />
                    </Col>
                  </Row>
                </Tabs.TabPane>
                <Tabs.TabPane tab={window.i18n("word.events")} key="2">
                  <Row justify="end" style={{marginBottom: '1%'}} >
                    <Col>
                      <FormButtonModal buttonIcon={<PlusOutlined style={{ fontSize: '20px'}}/>} title={window.i18n('title.newEvent')} formId='newEvent'>
                        <CreateEventForm eventTypes={this.state.eventTypes} eventStatuses={this.state.eventStatuses} onFinish={this.submitEvent}/>
                      </FormButtonModal>
                    </Col>
                  </Row>
                  <Row>
                    <Col span="24">
                      <Table dataSource={this.state.eventsTableData} columns={this.getEventsTableColumn()} pagination={false} bordered />
                    </Col>
                  </Row>
                </Tabs.TabPane>
              </Tabs>
            </div>
          </Col>
        </Row>
      </>
    )
  }
}
