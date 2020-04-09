import React from "react";
import { FreeSlot } from "./FreeSlot";

export default function Slots({
  freeSlotList,
  coupons,
  claimAppointment,
  selectAppointment,
  selectedAppointment,
  showSpinner,
  onClickSpinner,
}) {
  const renderFreeSlot = (slot) => {
    const sdt = slot.startDateTime;
    const slotLengthMin = slot.timeSlotLength;
    return (
      <FreeSlot
        key={sdt}
        startDateTime={sdt}
        slotLengthMin={slotLengthMin}
        freeAppointments={slot.freeAppointments}
        disable={coupons <= 0}
        highlight={selectedAppointment.startDateTime === sdt}
        claimAppointment={() => claimAppointment(sdt, slotLengthMin)}
        onFocus={() => selectAppointment(sdt, slotLengthMin)}
      />
    );
  };

  function renderNoMoreFreeSlotsError() {
    return (
      <div className="card warning fluid">
        <div>
          Aktuell sind{" "}
          <b>
            <u>keine Termine</u>
          </b>{" "}
          mehr frei.
        </div>
        <div
          dangerouslySetInnerHTML={{
            __html: window.config.contactInfoAppointment,
          }}
        />
      </div>
    );
  }

  function renderTable() {
    return (
      <table style={{ maxHeight: "91vh", marginTop: "1vh" }}>
        <thead>
          <tr>
            <th>Datum</th>
            <th>Terminslot</th>
            <th>Freie Termine</th>
            <th>
              <div className="container">
                <div className="row">
                  <div className="col-lg-6">Aktion</div>
                  <div
                    className="col-lg-6"
                    style={{
                      position: "absolute",
                      top: "var(--universal-padding)",
                      right: "var(--universal-padding)",
                    }}
                  >
                    <span
                      className={
                        showSpinner ? "icon-refresh animated" : "icon-refresh"
                      }
                      style={{
                        position: "absolute",
                        top: "var(--universal-padding)",
                        right: "var(--universal-padding)",
                        height: "1.6rem",
                        width: "1.6rem",
                      }}
                      onClick={onClickSpinner}
                    ></span>
                  </div>
                </div>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>{freeSlotList.map(renderFreeSlot)}</tbody>
      </table>
    );
  }

  return (
    <>
      {freeSlotList === null
        ? ""
        : freeSlotList.length > 0
        ? renderTable()
        : renderNoMoreFreeSlotsError()}
    </>
  );
}
