import React from 'react';
import { Row, Col, Table, Space, Button, Form, Popconfirm, DatePicker } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

import { getCommentsForHive, postCommentForHive, putComment, deleteComment } from '../services/aristaeus/comments';

import { LOADING_STATUS, getGenericPage } from '../pages/generic';
import { dealWithError, notificate } from '../lib/common';

import { FormLinkModal, FormButtonModal, RichEditor } from '.';

function CreateCommentForm(props) {
  const [form] = Form.useForm();

  const editorRef = React.useRef(null);

  const onFinish = (data) => {
    data.comment = editorRef.current.getContent();
    props.onFinish(data);
    form.resetFields();
  }

  return (
    <Form id="newComment" form={form} layout="vertical" requiredMark={false} onFinish={onFinish} onFailed={() => notificate("error", "Failed")}>
      <Form.Item label={window.i18n("word.date")} name="date">
        <DatePicker />
      </Form.Item>
      <Form.Item label={window.i18n("word.comment")} name="comment">
        <RichEditor editorRef={editorRef} />
      </Form.Item>
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

  const onFinish = (data) => {
    data.comment = editorRef.current.getContent();
    props.onFinish(data);
  }

  const editorRef = React.useRef(null);

  return (
    <Form id={props.formId} form={form} onFinish={onFinish} layout="vertical" requiredMark={false} onFailed={() => notificate("error", "Failed")}>
      <Form.Item label={window.i18n("word.date")} name="date">
        <DatePicker format="L" />
      </Form.Item>
      <Form.Item label={window.i18n("word.comment")} name="comment">
        <RichEditor defaultContent={props.content} editorRef={editorRef} />
      </Form.Item>
      <Form.Item name="commentId" hidden/>
    </Form>
  )
}


export class CommentTableComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pageStatus: LOADING_STATUS,
      commentsTableData: [],
    }
  }

  async componentDidMount() {
    try {
      let comments = await getCommentsForHive(this.props.hiveId);
      let commentsTableData = this.getCommentsTableData(comments);

      let pageStatus = "OK"
      this.setState({commentsTableData, pageStatus});

    } catch (error) {
      let status = dealWithError(error);

      this.setState((state) => {
        state['pageStatus'] = status;
        return state;
      })
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
          return <div dangerouslySetInnerHTML={{__html: text}} />
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
                <UpdateCommentForm formId={formId} onFinish={this.updateComment} commentId={record.id} date={record.date} content={record.comment} />
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

  submitComment = async(data) => {
    if (!data.date || !data.comment) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    let date = data.date.toISOString();
    let comment = data.comment;

    try {
      await postCommentForHive(this.props.hiveId, {date, comment})
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

  updateComment = async(data) => {
    if (!data.date || !data.comment) {
      notificate('error', window.i18n('error.incorrectEntry'))
      return;
    }

    let commentId = data.commentId;
    let date = data.date.toISOString();
    let comment = data.comment;

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

  render() {
    let genericPage = getGenericPage(this.state.pageStatus);
    if (genericPage) { return genericPage };

    return (
      <>
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
      </>
    );
  }
}