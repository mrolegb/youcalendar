/* eslint-disable require-jsdoc */
import styles from './Channels.module.css';
import React from 'react';
import {addChannel, deleteChannel} from '../api/channels';

class ChannelsForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      title: '',
      channelId: '',
      response: '',
    };

    this.handleAdd = this.handleAdd.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  async handleAdd(event) {
    event.preventDefault();
    const response = await addChannel(this.state.title, this.state.channelId);
    const r = await response.json();
    if (r) {
      this.setState({
        title: event.target.title,
        channelId: event.target.channelId,
        response: r.message,
      });
    }
  }

  async handleDelete(event) {
    event.preventDefault();
    const response = await deleteChannel(this.state.channelId);
    const r = await response.json();
    if (r) {
      this.setState({
        title: event.target.title,
        channelId: event.target.channelId,
        response: r.message,
      });
    }
  }

  render() {
    return (
      <div className={styles.Form}>
        <label>{this.state.response}</label>
        <form>
          <label className={styles.Field}>
            Channel title:
            <input type='text' name='title'
              value={this.state.title} onChange={this.handleChange}
            />
          </label>
          <label className={styles.Field}>
            Channel ID:
            <input type='text' name='channelId'
              value={this.state.channelId} onChange={this.handleChange}
            />
          </label>
          <p>
            <input
              className={styles.Field}
              type='submit'
              name='add'
              value='Add channel'
              onClick={this.handleAdd}
            />
            <input
              className={styles.Field}
              type='submit'
              name='delete'
              value='Delete channel'
              onClick={this.handleDelete}
            />
          </p>
        </form>
      </div>
    );
  }
}

export default ChannelsForm;
