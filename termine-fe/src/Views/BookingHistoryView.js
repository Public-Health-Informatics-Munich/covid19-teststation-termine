import {
  formatDate,
  formatStartTime,
  ISOStringWithoutTimeZone,
} from "../utils";
import React from "react";
import { Calendar } from "react-calendar";
import { Trans, t } from "@lingui/macro";
import config from "../config";
import "react-calendar/dist/Calendar.css";

export default function BookingHistoryView({
  i18n,
  bookedList,
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  onDeleteBooking,
}) {
  return (
    <div className="col">
      <div className="row">
        <label htmlFor="start">
          <Trans>From</Trans>
        </label>
        <Calendar
          id="start"
          onChange={(date) => setStartDate(date)}
          value={startDate}
        />

        <label htmlFor="end">
          <Trans>To</Trans>
        </label>
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
          <Trans>Excel</Trans>
        </a>
        <input
          type="button"
          value={i18n._(t`Print`)}
          onClick={() => {
            window.print();
            return false;
          }}
        />
      </div>
      <table className="dataTable printme" id="printme">
        <thead>
          <tr>
            <th>
              <Trans>Date of Appointment</Trans>
            </th>
            <th>
              <Trans>Booked at</Trans>
            </th>
            <th>
              <Trans>Surname</Trans>
            </th>
            <th>
              <Trans>Given Name</Trans>
            </th>
            <th>
              <Trans>Mobile No.</Trans>
            </th>
            <th>
              <Trans>Access Code</Trans>
            </th>
            <th></th>
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
                <td align="right">
                  <button
                    type="button"
                    className="secondary"
                    onClick={() => {
                      if (
                        window.confirm(
                          "Wollen Sie die Buchung wirklich löschen? Dies kann nicht rückgängig gemacht werden."
                        )
                      ) {
                        onDeleteBooking(booking.booking_id);
                        console.log("Confirmed");
                      }
                    }}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
