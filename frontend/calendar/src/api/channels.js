/* eslint-disable require-jsdoc */
import {request} from './api';


const URL = process.env.REACT_APP_LOCALHOST + '/channels';

export async function getChannels() {
  const response = await request(URL, 'GET', {}, {
    'Content-Type': 'application/json',
  });
  return response;
}

export async function addChannel(
    title='Zizaran',
    channelId='UCAG3CiKOUkQysyKCXSFEBPA',
) {
  const response = await request(URL, 'POST', {
    'title': title,
    'channel_id': channelId,
  }, {
    'Content-Type': 'application/json',
    'Authorize': process.env.REACT_APP_AUTH_KEY,
  });
  return response;
}

export async function deleteChannel(
    channelId='UCAG3CiKOUkQysyKCXSFEBPA',
) {
  const response = await request(URL, 'DELETE', {
    'channel_id': channelId,
  }, {
    'Content-Type': 'application/json',
    'Authorize': process.env.REACT_APP_AUTH_KEY,
  });
  return response;
}
