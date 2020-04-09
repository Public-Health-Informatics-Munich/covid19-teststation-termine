import {formatDate, formatTime, INFOBOX_STATES} from "../utils";
import React from "react";

export const InfoBox = ({infoboxState, errorMessage, selectedAppointment, bookedAppointment, secret}) => {
    return <div id="messages">
        {infoboxState === INFOBOX_STATES.ERROR && <div className="card error fluid">
            <div className="section">
                <h3 className="doc">Es ist ein Fehler aufgetreten</h3><p className="doc">{errorMessage}</p></div>
        </div>}
        {infoboxState === INFOBOX_STATES.APPOINTMENT_SUCCESS && <div className="card success fluid">
            <div className="section">
                <h3 className="doc">Termin für den {formatDate(bookedAppointment.startDateTime)}, {formatTime(bookedAppointment.startDateTime, bookedAppointment.lengthMin)} wurde
                    gebucht</h3><p className="doc">Teilen Sie dem Patienten jetzt den Berechtigungscode mit:</p><h3>
                <code>{secret}</code></h3></div>
        </div>}
        {infoboxState === INFOBOX_STATES.FORM_INPUT && <div className="card fluid">
            <div className="section">
                <h3 className="doc">Tragen Sie die Daten für
                    den {formatDate(selectedAppointment.startDateTime)}, {formatTime(selectedAppointment.startDateTime,
                        selectedAppointment.lengthMin)} ein</h3><p
                className="doc">Alle Felder sind Pflichtfelder.</p></div>
        </div>}
        {infoboxState === INFOBOX_STATES.INITIAL && <div className="card fluid">
            <div className="section">
                <h3 className="doc">Wählen Sie einen Termin aus</h3>
                <p className="doc">In der Tabelle kann mit Tab und Enter navigiert werden.</p></div>
        </div>}
    </div>;
}
