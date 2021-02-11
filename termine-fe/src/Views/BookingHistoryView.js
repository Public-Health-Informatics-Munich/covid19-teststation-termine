import {
  formatDate,
  formatStartTime,
  ISOStringWithoutTimeZone,
} from "../utils";
import { ErrorBox } from "../Components/ErrorBox";
import React from "react";
import { Calendar } from "react-calendar";
import { Trans, t } from "@lingui/macro";
import axios from "axios";
import config from "../config";
import "react-calendar/dist/Calendar.css";
import { ButtonWithConfirm } from "../Components/ButtonWithConfirm";

export default function BookingHistoryView({
  i18n,
  bookedList,
  startDate,
  setStartDate,
  errorMessage,
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
        <input
          type="button"
          value={i18n._(t`Excel`)}
          onClick={() => {
            axios
              .get(
                `${
                  config.API_BASE_URL
                }/booking_list.xlsx?start_date=${ISOStringWithoutTimeZone(
                  startDate
                )}&end_date=${ISOStringWithoutTimeZone(endDate)}`,
                {
                  method: "GET",
                  responseType: "blob",
                }
              )
              .then((response) => {
                const url = window.URL.createObjectURL(
                  new Blob([response.data])
                );
                const link = document.createElement("a");
                link.href = url;
                link.setAttribute("download", "booking_list.xlsx"); //or any other extension
                document.body.appendChild(link);
                link.click();
              });
          }}
        />
        <input
          type="button"
          value={i18n._(t`Print`)}
          onClick={() => {
            window.print();
            return false;
          }}
        />
      </div>
      <div>
        {errorMessage !== "" && <ErrorBox errorMessage={errorMessage} />}
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
                <td className="cellAlignRight">
                  <ButtonWithConfirm
                    i18n={i18n}
                    booking={booking}
                    onDeleteBooking={onDeleteBooking}
                  />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
