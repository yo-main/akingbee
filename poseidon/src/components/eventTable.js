import React from 'react';
import { Row, Col, Table, Space, Button, Form, Input, Popconfirm, Select, DatePicker } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

import { getEvents, postEvent, putEvent, deleteEvent } from '../services/aristaeus/events';
import { getSetupData } from '../services/aristaeus/setup';

import { LOADING_STATUS, getGenericPage } from '../pages/generic';
import { dealWithError, notificate } from '../lib/common';

import { FormLinkModal, FormButtonModal, RichEditor, EditorReadOnly } from '.';

function CreateEventForm(props) {
  const [form] = Form.useForm();

  const editorRef = React.useRef(null);

  const onFinish = (data) => {
    data.description = editorRef.current.getContent();
    props.onFinish(data);
    form.resetFields();
  }

  return (
    <Form id="newEvent" form={form} layout="vertical" requiredMark={false} onFinish={onFinish} onFailed={() => notificate("error", "Failed")}>
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
        <RichEditor editorRef={editorRef} />
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

  const editorRef = React.useRef(null);

  const onFinish = (data) => {
    data.description = editorRef.current.getContent();
    props.onFinish(data);
  }

  return (
    <Form id={props.formId} form={form} layout="vertical" requiredMark={false} onFinish={onFinish} onFailed={() => notificate("error", "Failed")}>
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
        <RichEditor defaultContent={props.description} editorRef={editorRef} />
      </Form.Item>
      <Form.Item name="eventId" hidden/>
    </Form>
  )
}


export class EventTableComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pageStatus: LOADING_STATUS,
      eventsTableData: [],
      eventStatuses: [],
      eventTypes: [],
    }
  }

  async componentDidMount() {
    try {
      let events = await getEvents(this.props.hiveId);
      let eventTypes = await getSetupData('event_type');
      let eventStatuses = await getSetupData('event_status');
      let eventsTableData = this.getEventsTableData(events);

      let pageStatus = "OK"
      this.setState({eventsTableData, eventStatuses, eventTypes, pageStatus});

    } catch (error) {
      let status = dealWithError(error);

      this.setState((state) => {
        state['pageStatus'] = status;
        return state;
      })
    }
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
          return <div dangerouslySetInnerHTML={{__html: JSON.parse(text)}} />
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

    return (
      <>
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
      </>
    );
  }
}
