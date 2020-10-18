import React from 'react';

import { Row, Col, Table, Space, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons'

import { Modal, AddNewData } from '../components';
import { getData, postNewData } from '../services/aristaeus/setup';

export class SetupPage extends React.Component {
  state = { visible: false, tableData: []}

  showModal = () => {
    this.setState((state) => ({
      visible: true,
      tableData: state.tableData,
    }))
  };

  closeModal = e => {
    this.setState((state) => ({
      visible: false,
      tableData: state.tableData,
    }))
  };

  dataCallback = (data) => {
    this.setState((state) => ({
      visible: state.visible, tableData: data
    }));
  }

  componentDidMount() {
    getData(this.props.dataType, this.dataCallback);
  }

  render() {

    const columns = [
      {
        title: window.i18n(`title.${this.props.dataType}`),
        dataIndex: 'name',
        key: 'name',
      },
    ];

    columns.push({
      title: window.i18n('word.actions'),
      key: 'action',
      render: (text, record) => (
        <Space size='middle'>
          <a>{window.i18n('word.edit')}</a>
          <a>{window.i18n('word.delete')}</a>
        </Space>
      )
    })

    return (
      <>
        <Row>
          <Col offset={2}>
            <Table dataSource={this.state.tableData} columns={columns} pagination={false} bordered />
          </Col>
          <Col style={{ paddingLeft: '20px'}}>
            <Button onClick={this.showModal}>
              <PlusOutlined />
            </Button>
          </Col>
        </Row>
        <Modal title='Test' visible={this.state.visible} closeModal={this.closeModal} formId='addNewDataFormId'>
          <AddNewData dataType={this.props.dataType} onFinish={postNewData} />
        </Modal>
      </>
    )
  }
}