import {formatDate, formatTime} from "../utils";
import React from "react";

export const FreeSlot = ({startDateTime, slotLengthMin, freeAppointments, disable, claimAppointment, onFocus, highlight}) => {

    const dataAutoFocus = highlight ? {"data-autofocus": true} : {};

    return <tr className={highlight ? "active" : ""}>
        <td style={{fontSize: "1.2em", display: "flex", alignItems: "center"}}>{formatDate(startDateTime)}</td>
        <td style={{fontSize: "1.2em", display: "flex", alignItems: "center"}}>{formatTime(startDateTime, slotLengthMin)}</td>
        <td style={{fontSize: "1.2em", display: "flex", alignItems: "center"}}>{freeAppointments}</td>
        <td><input type="button" className="primary" value="Termin Buchen" onClick={claimAppointment} {...dataAutoFocus}
                   onFocus={onFocus} disabled={disable}/></td>
    </tr>
}
