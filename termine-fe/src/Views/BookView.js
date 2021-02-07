import FocusLock from "react-focus-lock";
import Slots from "../Components/Slots";
import { InfoBox } from "../Components/InfoBox";
import { CouponBox } from "../Components/CouponBox";
import Booking from "../Components/Booking";
import React from "react";

export default function BookView({
  i18n,
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
  form,
  inputRef,
}) {
  return (
    <div className="row">
      <div className="col-lg-7">
        <FocusLock group="booking-workflow" disabled={!focusOnList}>
          <Slots
            i18n={i18n}
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
              i18n={i18n}
              onBook={onBook}
              onCancel={onCancelBooking}
              claimToken={claimToken}
              startDateTime={startDateTime}
              disable={focusOnList}
              form={form}
              inputRef={inputRef}
              infoboxState={infoboxState.state}
            />
          </div>
        </FocusLock>
      </div>
    </div>
  );
}
