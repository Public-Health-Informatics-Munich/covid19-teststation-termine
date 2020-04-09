import React, { useEffect, useCallback, useRef, useState } from "react";
import FocusLock from "react-focus-lock";
import { trackPromise, usePromiseTracker } from "react-promise-tracker";

import * as Api from "./Api";

function App() {
  const { promiseInProgress } = usePromiseTracker();

  const [triggerRefresh, setTriggerRefresh] = useState(true);
  const [showSpinner, setShowSpinner] = useState(promiseInProgress);
  const [userList, setUserList] = useState({});

  const editedUser = useRef(null);
  const editedUserTouched = useRef(false);

  const getUserListData = useCallback(() => {
    return Api.fetchUsers()
      .then((response) => {
        if (response.status === 200) {
          setUserList(
            response.data.reduce((acc, user) => {
              acc[user.user_name] = user;
              return acc;
            }, {})
          );
        }
      })
      .catch((error) => {
        //TODO: error handling
      });
  }, []);

  const patchUser = useCallback((data) => {
    return Api.patchUser(data)
      .then((response) => {
        if (response.status === 200) {
          refreshList();
        }
      })
      .catch((error) => {
        //TODO: error handling
        refreshList();
      });
  }, []);

  const refreshList = () => setTriggerRefresh(true);

  // refresh on triggerRefresh reset, then every 60 sec
  useEffect(() => {
    let interval = null;

    if (triggerRefresh) trackPromise(getUserListData());
    setTriggerRefresh(false);

    interval = setInterval(() => {
      trackPromise(getUserListData());
    }, 60000);

    return () => clearInterval(interval);
  }, [triggerRefresh, getUserListData]);

  // let the spinner animation run for 1.25 secs
  useEffect(() => {
    let timeout = null;

    if (promiseInProgress) {
      setShowSpinner(true);
    } else if (showSpinner) {
      setTimeout(() => setShowSpinner(false), 1250);
    }

    return () => clearTimeout(timeout);
  }, [showSpinner, promiseInProgress]);

  const setEditedUser = useCallback(
    (user) => {
      editedUser.current = { ...user };
    },
    [editedUser]
  );

  const patchEditedUser = useCallback(
    (e) => {
      editedUserTouched.current = true;
      setEditedUser({ ...editedUser.current, [e.target.id]: e.target.value });
      setUserList({
        ...userList,
        [editedUser.current.user_name]: editedUser.current,
      });
    },
    [editedUser, editedUserTouched, setEditedUser, userList]
  );

  const saveEditedUser = useCallback(() => {
    if (editedUserTouched.current) {
      patchUser({ ...editedUser.current }).then(
        () => (editedUserTouched.current = false)
      );
    }
  }, [editedUser, editedUserTouched, patchUser]);

  const ENTER_KEY = 13;

  const onEnterSave = useCallback(
    (e) => {
      if (e.keyCode === ENTER_KEY) {
        saveEditedUser();
      }
    },
    [saveEditedUser]
  );

  return (
    <div className="container">
      <header>
        <h3 style={{ paddingLeft: "var(--universal-padding)" }}>
          {window.config.longInstanceName}
        </h3>
      </header>
      <div className="row">
        <FocusLock group="booking-workflow">
          <form>
            <h3>Neuen Benutzer anlegen:</h3>
            <input
              type="text"
              name="new_user_name"
              placeholder="Benutzername"
              value=""
            />
            <input
              type="password"
              name="new_user_password"
              placeholder="Passwort"
              value=""
            />
            <input
              type="password"
              name="new_user_password_confirm"
              placeholder="Passwortverifikation"
              value=""
            />
            <input type="button" name="submit" value="Speichern" />
          </form>
        </FocusLock>
      </div>
      <div className="row">
        <div className="col-lg-12">
          <FocusLock group="booking-workflow">
            <table style={{ maxHeight: "98vh", marginTop: "1vh" }}>
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Administrator</th>
                  <th>Termine gebucht (total)</th>
                  <th>
                    <div className="container">
                      <div className="row">
                        <div className="col-lg-6">Verfügbare Termine</div>
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
                              showSpinner
                                ? "icon-refresh animated"
                                : "icon-refresh"
                            }
                            style={{
                              position: "absolute",
                              top: "var(--universal-padding)",
                              right: "var(--universal-padding)",
                              height: "1.6rem",
                              width: "1.6rem",
                            }}
                            onClick={refreshList}
                          ></span>
                        </div>
                      </div>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody>
                {Object.values(userList).map((user) => {
                  const style = {
                    fontSize: "1.2em",
                    display: "flex",
                    alignItems: "center",
                  };
                  return (
                    <tr className={false ? "active" : ""} key={user.user_name}>
                      <td style={style}>{user.user_name}</td>
                      <td style={style}>
                        <input
                          id="is_admin"
                          disabled={true}
                          type="checkbox"
                          checked={user.is_admin}
                          onChange={(e) =>
                            patchUser({
                              ...user,
                              is_admin: e.target.value || false,
                            })
                          }
                        />
                      </td>
                      <td style={style}>{user.total_bookings}</td>
                      <td style={style}>
                        <input
                          id="coupons"
                          type="number"
                          min="0"
                          value={user.coupons}
                          onFocus={(e) => setEditedUser(user)}
                          onBlur={saveEditedUser}
                          onChange={patchEditedUser}
                          onKeyDown={onEnterSave}
                        />
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </FocusLock>
        </div>
      </div>
    </div>
  );
}

export default App;
