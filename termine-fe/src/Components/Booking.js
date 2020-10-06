import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { Trans, t } from "@lingui/macro";
import { INFOBOX_STATES } from "../utils";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import "react-datepicker/dist/react-datepicker.css";
let reasons = require("../locales/de/reasons.json");

const renderInputRequired = () => (
  <span className="hintLabel">
    <Trans>This input is required.</Trans>
  </span>
);

export default function Booking({
  i18n,
  onBook,
  onCancel,
  startDateTime,
  claimToken,
  disable,
  state,
  setState,
  inputRef,
}) {
  const [startDate, setStartDate] = useState(new Date("1990-01-01"));
  const { register, handleSubmit, reset, errors } = useForm();

  const updateField = (e) => {
    setState({
      ...state,
      [e.target.id]: e.target.value,
    });
  };

  const updateDayOfBirth = (date) => {
    setState({
      ...state,
      dayOfBirth: format(date, "yyyy-MM-dd"),
    });
  };

  const onFocusHandler = () => {
    setState({
      ...state,
      infoboxState: INFOBOX_STATES.FORM_INPUT,
    });
  };

  const localOnBook = (_) => {
    onBook({ ...state, claimToken, startDateTime });
  };

  const {
    office,
    firstName,
    name,
    street,
    streetNumber,
    postCode,
    city,
    phone,
    dayOfBirth,
    reason,
  } = state;

  const reasonItems = reasons.map((value) => (
    <option value={value}>{value}</option>
  ));

  return (
    <form
      className={disable ? "disabled" : ""}
      onSubmit={handleSubmit(localOnBook)}
      ref={inputRef}
      onFocus={() => onFocusHandler()}
    >
      <fieldset className="input-group vertical">
        <legend>
          <Trans>Booking</Trans>
        </legend>
        <label htmlFor="firstName" className="displayFlex">
          <Trans>Given Name</Trans> {errors.firstName && renderInputRequired()}
        </label>
        <input
          id="firstName"
          name="firstName"
          readOnly={disable}
          disabled={disable}
          onChange={updateField}
          value={firstName}
          ref={register({ required: true })}
        />
        <label htmlFor="name" className="displayFlex">
          <Trans>Surname</Trans> {errors.name && renderInputRequired()}
        </label>
        <input
          id="name"
          name="name"
          readOnly={disable}
          disabled={disable}
          onChange={updateField}
          value={name}
          ref={register({ required: true })}
        />
        <fieldset className="input-group vertical">
          <legend>
            <Trans>Home Address</Trans>
          </legend>
          <div className="displayFlex vertical">
            <div className="displayFlex">
              <div className="displayFlex vertical weight-12">
                <label htmlFor="street">
                  <Trans>Street</Trans> {errors.name && renderInputRequired()}
                </label>
                <input
                  id="street"
                  name="street"
                  readOnly={disable}
                  disabled={disable}
                  onChange={updateField}
                  value={street}
                  ref={register({ required: true })}
                />
              </div>
              <div className="displayFlex vertical weight-1">
                <label htmlFor="streetnumber">
                  <Trans>StreetNumber</Trans>{" "}
                  {errors.name && renderInputRequired()}
                </label>
                <input
                  id="streetNumber"
                  name="streetNumber"
                  readOnly={disable}
                  disabled={disable}
                  onChange={updateField}
                  value={streetNumber}
                  ref={register({ required: true })}
                />
              </div>
            </div>
            <div className="displayFlex">
              <div className="displayFlex vertical weight-1">
                <label htmlFor="postCode">
                  <Trans>PostCode</Trans> {errors.name && renderInputRequired()}
                </label>
                <input
                  type="number"
                  id="postCode"
                  name="postCode"
                  readOnly={disable}
                  disabled={disable}
                  onChange={updateField}
                  value={postCode}
                  ref={register({ required: true })}
                />
              </div>
              <div className="displayFlex vertical weight-12">
                <label htmlFor="city">
                  <Trans>City</Trans> {errors.name && renderInputRequired()}
                </label>
                <input
                  id="city"
                  name="city"
                  readOnly={disable}
                  disabled={disable}
                  onChange={updateField}
                  value={city}
                  ref={register({ required: true })}
                />
              </div>
            </div>
          </div>
        </fieldset>
        <label htmlFor="phone" className="displayFlex">
          <Trans>Mobile No.</Trans> {errors.phone && renderInputRequired()}
        </label>
        <input
          type="number"
          id="phone"
          name="phone"
          readOnly={disable}
          disabled={disable}
          onChange={updateField}
          value={phone}
          ref={register({ required: true })}
        />
        <label htmlFor="dayOfBirth" className="displayFlex">
          <Trans>DayOfBirth</Trans> {errors.phone && renderInputRequired()}
        </label>
        <DatePicker
          id="dayOfBirth"
          name="dayOfBirth"
          showYearDropdown
          showMonthDropdown
          dropdownMode="select"
          maxDate={new Date()}
          selected={startDate}
          onChange={(date) => {
            setStartDate(date);
            updateDayOfBirth(date);
            console.log(state.dayOfBirth);
          }}
        />
        <label htmlFor="office" className="displayFlex">
          <Trans>Office</Trans> {errors.office && renderInputRequired()}
        </label>
        <input
          id="office"
          name="office"
          readOnly={disable}
          disabled={disable}
          onChange={updateField}
          value={office}
          ref={register({ required: true })}
        />
        <label htmlFor="reason" className="displayFlex">
          <Trans>Reason</Trans> {errors.office && renderInputRequired()}
        </label>
        <select
          id="reason"
          name="reason"
          onChange={updateField}
          ref={register({ required: true })}
        >
          {reasonItems}
        </select>
        <input
          type="submit"
          className="primary"
          id="submit"
          value={i18n._(t`Book Appointment`)}
          disabled={disable}
          style={{ fontSize: "1.2em" }}
        />
        <input
          type="button"
          className="secondary"
          id="cancel"
          value={i18n._(t`Cancel`)}
          disabled={disable}
          style={{ fontSize: "1.2em" }}
          onClick={() => {
            reset();
            onCancel();
          }}
        />
      </fieldset>
    </form>
  );
}
