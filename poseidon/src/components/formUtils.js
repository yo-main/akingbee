import React from 'react';

import { Button, Form, Space, Row, Col } from 'antd';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons'

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