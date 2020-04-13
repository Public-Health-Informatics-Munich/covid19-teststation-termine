import { formatDate, formatTime, INFOBOX_STATES } from "../utils";
import React from "react";
import { Trans } from "@lingui/macro";

export const InfoBox = ({
  infoboxState,
  errorMessage,
  selectedAppointment,
  bookedAppointment,
  secret,
}) => {
  return (
    <div id="messages">
      {infoboxState === INFOBOX_STATES.ERROR && (
        <div className="card error fluid">
          <div className="section">
            <h3 className="doc">
              <Trans>An error occurred</Trans>
            </h3>
            <p className="doc">{errorMessage}</p>
          </div>
        </div>
      )}
      {infoboxState === INFOBOX_STATES.APPOINTMENT_SUCCESS && (
        <div className="card success fluid">
          <div className="section">
            <h3 className="doc">
              <Trans>
                Appointment for the{" "}
                {formatDate(bookedAppointment.startDateTime)},{" "}
                {formatTime(
                  bookedAppointment.startDateTime,
                  bookedAppointment.lengthMin
                )}{" "}
                has been booked
              </Trans>
            </h3>
            <p className="doc">
              <Trans>Notify the patient of their access code:</Trans>
            </p>
            <h3>
              <code>{secret}</code>
            </h3>
          </div>
        </div>
      )}
      {infoboxState === INFOBOX_STATES.FORM_INPUT && (
        <div className="card fluid">
          <div className="section">
            <h3 className="doc">
              <Trans>
                Enter the information for the{" "}
                {formatDate(selectedAppointment.startDateTime)},{" "}
                {formatTime(
                  selectedAppointment.startDateTime,
                  selectedAppointment.lengthMin
                )}
              </Trans>
            </h3>
            <p className="doc">
              <Trans>All fields are required.</Trans>
            </p>
          </div>
        </div>
      )}
      {infoboxState === INFOBOX_STATES.INITIAL && (
        <div className="card fluid">
          <div className="section">
            <h3 className="doc">
              <Trans>Choose an appointment</Trans>
            </h3>
            <p className="doc">
              <Trans>
                The navigation in the table is possible with Tab and Enter keys.
              </Trans>
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
