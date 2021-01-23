import React from 'react';

import { Button, Form, Space, Row, Col, Cascader } from 'antd';
import { PlusOutlined, MinusCircleOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons'

import { formItemLayoutWithoutLabel } from '../constants';

export const formItemLayoutOptional = {
  labelCol: {
    xs: { span: 24 },
    sm: { span: 8 },
  },
  wrapperCol: {
    xs: { span: 20 },
    sm: { span: 12 },
  },
};



export class OptionalFormItem extends React.Component {
  state = {
    active: false
  }

  setActive = () => {
    this.setState((state) => {
      state.active = true;
    })
    this.forceUpdate();
  }

  setInative = () => {
    this.setState((state) => {
      state.active = false;
    });
    this.forceUpdate();
  }

  render() {
    return (
      <>
        {this.state.active === false ?
          <Form.Item {...formItemLayoutWithoutLabel}>
            <Button
              type="dashed"
              onClick={this.setActive}
              icon={<PlusOutlined />}
            >
              {this.props.buttonName}
            </Button>
          </Form.Item>
        :
          <Row>
            <Col span='20'>
              <Form.Item {...this.props} style={{paddingLeft: '10%'}}>
                {this.props.children}
              </Form.Item>
            </Col>
            <Col>
              <MinusCircleOutlined
              onClick={this.setInative}
              style={{paddingTop: '70%', paddingLeft: '50%'}}
              />
            </Col>
          </Row>
        }
      </>
    )
  }
}



export class CascaderForm extends React.Component {
  state = {selected: false}

  render() {
    const onChange = (value) => {
      if (value.length > 0 && !this.state.selected) {
        this.setState({selected: true})
      } else if (value.length === 0 && this.state.selected) {
        this.setState({selected: false})
      }
    }

    let buttons;
    if (this.state.selected) {
      buttons = (
        <Form.Item>
          <Button htmlType='submit' icon={<CheckCircleOutlined/>} type='text' />
        </Form.Item>
      )
    }

    return (
      <Form {...this.props}>
        <Row>
          <Col>
            <Form.Item name="action">
              <Cascader options={this.props.options} onChange={onChange} placeholder={this.props.title}/>
            </Form.Item>
          </Col>
          <Col>
            {buttons}
          </Col>
        </Row>
      </Form>
    )
  }
}
