import React from 'react';

import { ReactComponent as NotFoundSvg } from '../images/404.svg';

import { Row } from 'antd';

import ClipLoader from "react-spinners/ClipLoader";

export const NOT_FOUND_STATUS = 'NOT_FOUND';
export const ERROR_STATUS = 'ERROR';
export const LOADING_STATUS = 'LOADING';

export function NotFound() {
  return (
    <>
    <Row justify="center" align="middle" style={{'min-height': '85vh'}}>
      <NotFoundSvg />
    </Row>
    </>
  )
}

function Loading() {
  return (
    <Row justify="center" align="middle" style={{'min-height': '85vh'}}>
      <ClipLoader color="#599BFF" size={75} />
    </Row>
  );
}

function Error() {
  return <p>We encountered an error, sorry</p>
}

export function getGenericPage(page_status) {
  switch (page_status) {
    case NOT_FOUND_STATUS:
      return <NotFound />;
    case ERROR_STATUS:
      return <Error />;
    case LOADING_STATUS:
      return <Loading />;
    default:
      return null;
  }
}