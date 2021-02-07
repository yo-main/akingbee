import React from 'react';

export const NOT_FOUND_STATUS = 'NOT_FOUND';
export const ERROR_STATUS = 'ERROR';
export const LOADING_STATUS = 'LOADING';

export function NotFound() {
  return <p>Sorry, nothing here</p>;
}

function Loading() {
  return <p>Loading</p>
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