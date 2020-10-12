import React from "react";
import { MdDeleteForever } from "react-icons/md";
import { withI18n } from "@lingui/react";
import { t } from "@lingui/macro";

export const ButtonWithConfirm = ({ i18n, booking, onDeleteBooking }) => (
  <button
    type="button"
    className="secondary icon"
    onClick={() => {
      if (
        window.confirm(
          i18n._(
            "Do you really want to delete this booking? This cannot be undone."
          )
        )
      ) {
        onDeleteBooking(booking.booking_id);
        console.log("Confirmed");
      }
    }}
  >
    <MdDeleteForever size="2em" />
  </button>
);
