import FocusLock from "react-focus-lock";
import Slots from "../Components/Slots";
import { InfoBox } from "../Components/InfoBox";
import { CouponBox } from "../Components/CouponBox";
import Booking from "../Components/Booking";
import React from "react";

export default function BookView({
  focusOnList,
  freeSlotList,
  coupons,
  claimAppointment,
  setSelectedAppointment,
  selectedAppointment,
  showSpinner,
  refreshList,
  infoboxState,
  bookedAppointment,
  onBook,
  onCancelBooking,
  claimToken,
  startDateTime,
  formState,
  setFormState,
  inputRef,
}) {
  return (
    <div className="row">
      <div className="col-lg-7">
        <FocusLock group="booking-workflow" disabled={!focusOnList}>
          <Slots
            freeSlotList={freeSlotList}
            coupons={coupons}
            claimAppointment={claimAppointment}
            selectAppointment={(app, lengthMin) =>
              setSelectedAppointment({
                startDateTime: app,
                lengthMin: lengthMin,
              })
            }
            selectedAppointment={selectedAppointment}
            showSpinner={showSpinner}
            onClickSpinner={refreshList}
          />
        </FocusLock>
      </div>
      <div className="col-lg-5">
        <FocusLock group="booking-workflow" disabled={focusOnList}>
          <div style={{ marginTop: "1vh" }}>
            <InfoBox
              infoboxState={infoboxState.state}
              selectedAppointment={selectedAppointment}
              bookedAppointment={bookedAppointment}
              errorMessage={infoboxState.msg}
              secret={infoboxState.msg}
            />
            <CouponBox coupons={coupons} />
            <Booking
              onBook={onBook}
              onCancel={onCancelBooking}
              claimToken={claimToken}
              startDateTime={startDateTime}
              disable={focusOnList}
              {...{ state: formState, setState: setFormState, inputRef }}
            />
          </div>
        </FocusLock>
      </div>
    </div>
  );
}
