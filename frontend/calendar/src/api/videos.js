/* eslint-disable require-jsdoc */
import {request} from './api';

const URL = process.env.REACT_APP_LOCALHOST + '/videos';

export async function getVideos(
    dateFrom='2022-10-01T16:34:58Z',
    dateTo='2022-10-21T16:34:58Z',
) {
  const response = await request(URL, 'POST', {
    'date_from': dateFrom,
    'date_to': dateTo,
  }, {
    'Content-Type': 'application/json',
    'Debug': 1,
  });
  return response;
}
