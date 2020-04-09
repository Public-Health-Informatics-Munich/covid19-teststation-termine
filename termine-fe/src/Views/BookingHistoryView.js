import {
  formatDate,
  formatStartTime,
  ISOStringWithoutTimeZone,
} from "../utils";
import React from "react";
import { Calendar } from "react-calendar";
import config from "../config";
import "react-calendar/dist/Calendar.css";

export default function BookingHistoryView(
  bookedList,
  startDate,
  setStartDate,
  endDate,
  setEndDate
) {
  return (
    <div className="col">
      <div className="row">
        <label htmlFor="start">Von</label>
        <Calendar
          id="start"
          onChange={(date) => setStartDate(date)}
          value={startDate}
        />

        <label htmlFor="end">Bis</label>
        <Calendar
          id="end"
          onChange={(date) => setEndDate(date)}
          value={endDate}
        />
      </div>
      <div className="row">
        <a
          href={`${
            config.API_BASE_URL
          }/booking_list.xlsx?start_date=${ISOStringWithoutTimeZone(
            startDate
          )}&end_date=${ISOStringWithoutTimeZone(endDate)}`}
          className="button"
          target="_blank"
          rel="noopener noreferrer"
        >
          Excel
        </a>
        <input
          type="button"
          value="Drucken"
          onClick={() => {
            window.print();
            return false;
          }}
        />
      </div>
      <table className="dataTable printme" id="printme">
        <thead>
          <tr>
            <th>Datum des Termins</th>
            <th>Gebucht am</th>
            <th>Name</th>
            <th>Vorname</th>
            <th>Handynummer</th>
            <th>Berechtigungscode</th>
          </tr>
        </thead>
        <tbody>
          {bookedList.map((booking, id) => {
            return (
              <tr key={booking.booked_at + id}>
                <td>
                  {formatDate(booking.start_date_time)}{" "}
                  {formatStartTime(booking.start_date_time)}
                </td>
                <td>
                  {formatDate(booking.booked_at)}{" "}
                  {formatStartTime(booking.booked_at)}
                </td>
                <td>{booking.surname}</td>
                <td>{booking.first_name}</td>
                <td>{booking.phone}</td>
                <td>{booking.secret}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
