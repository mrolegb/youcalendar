/* eslint-disable require-jsdoc */
import styles from './Videos.module.css';
import React from 'react';
import {getVideos} from '../api/videos';
import moment from 'moment';

const days = [
  'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
];

function getDates(week = 0) {
  const weekOffset = week * 7;
  const f = new Date();
  const l = new Date();
  const firstDay = new Date(
      f.setDate(f.getDate() - f.getDay() + 1 + weekOffset),
  );
  const lastDay = new Date(
      l.setDate(l.getDate() - l.getDay() + 7 + weekOffset),
  );
  return {
    date_from: firstDay,
    date_to: lastDay,
  };
}

class Videos extends React.Component {
  constructor(props) {
    super(props);
    const dates = getDates();
    this.state = {
      code: 0,
      status: '',
      data: null,
      headerDates: null,
      week: 0,
      date_from: dates.date_from,
      date_to: dates.date_to,
    };

    this.removeWeek = this.removeWeek.bind(this);
    this.addWeek = this.addWeek.bind(this);
  }

  async buildCalendar(currentWeek) {
    const dates = getDates(currentWeek);
    const videos = await getVideos(
        dates.date_from.toUTCString(), dates.date_to.toUTCString(),
    );
    const response = await videos.json();

    const data = [];
    if (videos.status === 200) {
      response.message.map((item) => {
        data.push(
            <div key={item.id} id={item.channelId}>
              <p>{item.title}
              + {Math.ceil(moment.duration(item.duration).asMinutes())}</p>
            </div>,
        );
      });
    }

    const headerDates = [];
    for (let i=0; i<7; i++) {
      const d = new Date(dates.date_from);
      d.setDate(d.getDate() + i);
      headerDates.push(
          <div key={i} className={styles.DateCell}>
            <div className={styles.WeekDay}>{days[i]}</div>
            {d.toLocaleDateString()}
          </div>,
      );
    }

    const grid = [];
    for (let i=0; i<24*7; i++) {
      grid.push(
          <div key={i} className={styles.GridCell}></div>,
      );
    }

    this.setState({
      code: videos.status,
      status: response.status,
      data: videos.status === 200 ? data : response.message,
      headerDates: headerDates,
      week: currentWeek,
      date_from: dates.date_from,
      date_to: dates.date_to,
      grid: grid,
    });

    document.getElementById('Calendar').scrollTo(
        {top: document.getElementById('Calendar').clientHeight / 2},
    );
  }

  async componentDidMount() {
    this.buildCalendar(this.state.week);
  }

  async removeWeek(event) {
    event.preventDefault();
    const week = this.state.week - 1;
    await this.buildCalendar(week);
  }

  async addWeek(event) {
    event.preventDefault();
    const week = this.state.week + 1;
    await this.buildCalendar(week);
  }

  render() {
    return (
      <><div>
        <div className={styles.Header}>
          <input
            className={styles.DateCell}
            type='submit'
            name='back'
            value='Back'
            onClick={this.removeWeek}
          />
          {this.state.headerDates}
          <input
            className={styles.DateCell}
            type='submit'
            name='forward'
            value='Forward'
            onClick={this.addWeek}
            disabled={this.state.week >= 0}
          />
        </div>
        <div className={styles.Calendar} id="Calendar">
          <div className={styles.CalendarRow}></div>
          <div className={styles.CalendarRow}>Dates</div>
          <div className={styles.CalendarRow}>
            <div className={styles.Grid}>{this.state.grid}</div>
          </div>
          <div className={styles.CalendarRow}>{this.state.data}</div>
        </div>
        <div className={styles.StatusBar}>
          {this.state.code} {this.state.status}
        </div>
      </div></>
    );
  }
};

export default Videos;
