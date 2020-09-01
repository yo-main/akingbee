import Head from 'next/head';
import { Component } from 'react';
import { Layout } from 'antd';
import { getSideMenu, getMainMenu } from './menu';

const { Header, Content, Footer } = Layout;

export default class Frame extends Component {
  constructor(props) {
    super(props);
    this.state = {}
  }

  getHead() {
    return (
      <Head>
        <title>aKingBee</title>
        <meta charSet="UTF-8" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <meta name="description" content="A website dedicated to bees and beekeepers" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
    )
  }

  getBody() {
    return (
      <>
        <Header className="header">
          <div className="logo" />
          {getMainMenu(this.props)}
        </Header>
        <Content style={{ padding: '0 50px' }}>
          <Layout className="site-layout-background" style={{ padding: '24px 0', height: '100vh' }}>
            {getSideMenu(this.props)}
            {this.getContent()}
          </Layout>
        </Content>
      </>
    );
  }

  getFooter() {
    return <Footer style={{ textAlign: 'center' }}>Ant Design ©2018 Created by Ant UED</Footer>;
  }

  getContent() {
    return <Content>Content</Content>;
  }

  render() {
    return (
      <Layout style={{height: '100%'}}>
        {this.getHead()}
        {this.getBody()}
        {this.getFooter()}
      </Layout>
    );
  }
}

