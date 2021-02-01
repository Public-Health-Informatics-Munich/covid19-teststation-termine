import React, {
  useEffect,
  useCallback,
  useRef,
  useState,
  useReducer,
} from "react";
import { trackPromise, usePromiseTracker } from "react-promise-tracker";
import {
  Switch,
  Route,
  Link,
  Redirect,
  useLocation,
  useHistory,
} from "react-router-dom";
import { Trans, t } from "@lingui/macro";
import { useForm } from "react-hook-form";
import { format } from "date-fns";
import { INFOBOX_STATES, ISOStringWithoutTimeZone } from "./utils";
import * as Api from "./Api";
import BookView from "./Views/BookView";
import BookingHistoryView from "./Views/BookingHistoryView";
import SettingsView from "./Views/SettingsView";
import { LoginView } from "./Views/LoginView";
import { ACTION_TYPES } from "./state/Actions";

const reducer = (state, action) => {
  switch (action.type) {
    case ACTION_TYPES.reset:
    case ACTION_TYPES.setLoggedOut:
      return initialState;
    case ACTION_TYPES.setLoggedIn:
      return { ...state, loggedIn: true };
    case ACTION_TYPES.setTriggerRefresh:
      return { ...state, triggerRefresh: action.value };
    case ACTION_TYPES.setSelectedAppointment:
      return { ...state, selectedAppointment: action.value };
    case ACTION_TYPES.setBookedAppointment:
      return { ...state, bookedAppointment: action.value };
    case ACTION_TYPES.setShowSpinner:
      return { ...state, showSpinner: action.value };
    case ACTION_TYPES.setFreeSlotList:
      return { ...state, freeSlotList: action.value };
    case ACTION_TYPES.setCoupons:
      return { ...state, coupons: action.value };
    case ACTION_TYPES.resetClaimToken:
      return { ...state, claimToken: initialState.claimToken };
    case ACTION_TYPES.setClaimToken:
      return { ...state, claimToken: action.value };
    case ACTION_TYPES.resetStartDateTime:
      return { ...state, startDateTime: initialState.startDateTime };
    case ACTION_TYPES.setStartDateTime:
      return { ...state, startDateTime: action.value };
    case ACTION_TYPES.setFocusOnList:
      return { ...state, focusOnList: action.value };
    case ACTION_TYPES.resetInfoboxState:
      return { ...state, infoboxState: initialState.infoboxState };
    case ACTION_TYPES.setInfoboxState:
      return { ...state, infoboxState: action.value };
    case ACTION_TYPES.setBookedList:
      return { ...state, bookedList: action.value };
    case ACTION_TYPES.setStartDate:
      return { ...state, startDate: action.value };
    case ACTION_TYPES.setEndDate:
      return { ...state, endDate: action.value };
    case ACTION_TYPES.setBookingHistoryErrorMessage:
      return { ...state, bookingHistoryErrorMessage: action.value };
    default:
      console.error(`unknown action: ${action}`);
  }
};

const initialState = {
  loggedIn: false,
  triggerRefresh: true,
  selectedAppointment: {
    startDateTime: "",
    lengthMin: 0,
  },
  bookedAppointment: {
    startDateTime: "",
    lengthMin: 0,
  },
  showSpinner: false,
  freeSlotList: null,
  coupons: null,
  claimToken: "",
  startDateTime: "",
  focusOnList: true,
  infoboxState: {
    state: INFOBOX_STATES.INITIAL,
    msg: "",
  },
  bookedList: [],
  startDate: new Date(),
  endDate: new Date(),
  bookingHistoryErrorMessage: "",
};

function App({ i18n }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  const {
    loggedIn,
    triggerRefresh,
    selectedAppointment,
    bookedAppointment,
    showSpinner,
    freeSlotList,
    coupons,
    claimToken,
    startDateTime,
    focusOnList,
    infoboxState,
    bookedList,
    startDate,
    endDate,
    bookingHistoryErrorMessage,
  } = state;

  const setSelectedAppointment = (appointment) => {
    dispatch({ type: ACTION_TYPES.setSelectedAppointment, value: appointment });
  };

  const setStartDate = (date) => {
    dispatch({ type: ACTION_TYPES.setStartDate, value: date });
  };
  const setEndDate = (date) => {
    dispatch({ type: ACTION_TYPES.setEndDate, value: date });
  };

  const useFocus = () => {
    const htmlElRef = useRef(null);
    const setFocus = useCallback(() => {
      htmlElRef.current && htmlElRef.current.focus();
    }, [htmlElRef]);
    return [htmlElRef, setFocus];
  };

  const TAB = {
    BOOK: "/book",
    BOOKED: "/booked",
    SETTINGS: "/settings",
  };

  let location = useLocation();

  const { promiseInProgress } = usePromiseTracker();

  const [inputRef, setInputFocus] = useFocus();

  const form = useForm();

  const history = useHistory();
  const getSlotListData = useCallback(() => {
    return Api.fetchSlots()
      .then((response) => {
        if (response.status === 200) {
          dispatch({
            type: ACTION_TYPES.setFreeSlotList,
            value: response.data.slots,
          });
          dispatch({
            type: ACTION_TYPES.setCoupons,
            value: response.data.coupons,
          });
        }
      })
      .catch(() => {
        //TODO: error handling
      });
  }, []);

  const getBookedListData = useCallback(() => {
    return Api.fetchBooked(
      ISOStringWithoutTimeZone(startDate),
      ISOStringWithoutTimeZone(endDate)
    )
      .then((response) => {
        if (response.status === 200) {
          dispatch({ type: ACTION_TYPES.setBookedList, value: response.data });
        }
      })
      .catch(() => {
        //TODO: error handling
      });
  }, [startDate, endDate]);

  const refreshList = () =>
    dispatch({ type: ACTION_TYPES.setTriggerRefresh, value: true });

  // use focusOnList as switch between slots table and form
  useEffect(() => {
    if (focusOnList) refreshList();
    else setInputFocus();
  }, [focusOnList, setInputFocus]);

  // use focusOnList as switch between slots table and form
  useEffect(() => {
    if (location.pathname === TAB.BOOKED) {
      getBookedListData();
    }
  }, [location, getBookedListData, TAB.BOOKED]);

  // refresh once on triggerRefresh, then every 60 sec
  useEffect(() => {
    if (loggedIn) {
      let interval = null;

      if (triggerRefresh) trackPromise(getSlotListData());
      dispatch({ type: ACTION_TYPES.setTriggerRefresh, value: false });

      interval = setInterval(() => {
        trackPromise(getSlotListData());
      }, 60000);

      return () => clearInterval(interval);
    }
  }, [triggerRefresh, getSlotListData, loggedIn]);

  // let the spinner animation run for 1.25 secs
  useEffect(() => {
    let timeout = null;

    if (promiseInProgress) {
      dispatch({ type: ACTION_TYPES.setShowSpinner, value: true });
    } else if (showSpinner) {
      setTimeout(
        () => dispatch({ type: ACTION_TYPES.setShowSpinner, value: false }),
        1250
      );
    }

    return () => clearTimeout(timeout);
  }, [showSpinner, promiseInProgress]);

  const claimAppointment = (startDateTime, slotLengthMin) => {
    if (claimToken !== "") {
      Api.unClaimSlot(claimToken).catch(() => {
        // TODO: error handling?
      });
    }
    return Api.claimSlot(startDateTime)
      .then((response) => {
        dispatch({
          type: ACTION_TYPES.setInfoboxState,
          value: {
            state: INFOBOX_STATES.FORM_INPUT,
            msg: "",
          },
        });
        dispatch({ type: ACTION_TYPES.setStartDateTime, value: startDateTime });
        setSelectedAppointment({
          startDateTime: startDateTime,
          lengthMin: slotLengthMin,
        });
        dispatch({ type: ACTION_TYPES.setClaimToken, value: response.data });
        form.reset();
        dispatch({ type: ACTION_TYPES.setFocusOnList, value: false });
      })
      .catch((error) => {
        dispatch({
          type: ACTION_TYPES.setInfoboxState,
          value: {
            state: INFOBOX_STATES.ERROR,
            msg:
              error.response?.status === 410
                ? i18n._(
                    t`The appointment is no longer available, please select another free appointment.`
                  )
                : i18n._(t`An unknown error occurred, please reload the page.`),
          },
        });
        dispatch({ type: ACTION_TYPES.resetStartDateTime });
        dispatch({ type: ACTION_TYPES.resetClaimToken });
        dispatch({ type: ACTION_TYPES.setFocusOnList, value: true });
      });
  };

  const onBook = (data) => {
    if (window.config.formFields.includes("dayOfBirth")) {
      data = {
        ...data,
        dayOfBirth: format(data.dayOfBirth, "yyyy-MM-dd"),
      };
    }

    Api.book(data)
      .then((response) => {
        dispatch({
          type: ACTION_TYPES.setInfoboxState,
          value: {
            state: INFOBOX_STATES.APPOINTMENT_SUCCESS,
            msg: response.data.secret,
          },
        });
        dispatch({
          type: ACTION_TYPES.setStartDateTime,
          value: response.data.time_slot,
        });
        dispatch({
          type: ACTION_TYPES.setBookedAppointment,
          value: {
            startDateTime: response.data.time_slot,
            lengthMin: response.data.slot_length_min,
          },
        });
        dispatch({ type: ACTION_TYPES.resetClaimToken });
        dispatch({ type: ACTION_TYPES.setFocusOnList, value: true });
      })
      .catch((error) => {
        dispatch({
          type: ACTION_TYPES.setInfoboxState,
          value: {
            state: INFOBOX_STATES.ERROR,
            msg:
              error.response.status === 410
                ? i18n._(
                    t`The appointment is no longer available, please select another free appointment.`
                  )
                : i18n._(t`An unknown error occurred, please reload the page.`),
          },
        });
        dispatch({ type: ACTION_TYPES.resetStartDateTime });
        dispatch({ type: ACTION_TYPES.resetClaimToken });
        dispatch({ type: ACTION_TYPES.setFocusOnList, value: true });
      });
  };

  const onCancelBooking = () => {
    Api.unClaimSlot(claimToken)
      .then(() => {
        dispatch({ type: ACTION_TYPES.resetInfoboxState });
        dispatch({ type: ACTION_TYPES.resetStartDateTime });
        dispatch({ type: ACTION_TYPES.resetClaimToken });
        dispatch({ type: ACTION_TYPES.setFocusOnList, value: true });
        form.reset();
      })
      .catch((error) => {
        //Todo handle error
        console.error(error);
      });
  };

  const onDeleteBooking = (id) => {
    Api.deleteBooking(id)
      .then((response) => {
        console.log(response.statusText);
        if (response.status === 200) {
          getBookedListData();
          dispatch({
            type: ACTION_TYPES.setBookingHistoryErrorMessage,
            value: "",
          });
        }
      })
      .catch((error) => {
        dispatch({
          type: ACTION_TYPES.setBookingHistoryErrorMessage,
          value: i18n._(
            t`Deleting the appointment did not work. Please contact your administrator.`
          ),
        });
      });
  };

  const login = ({ username, password }) => {
    Api.login(username, password).then((response) => {
      if (response.status === 200) {
        console.log(`JWT TOKEN: ${response.data}`);
        window.localStorage.setItem(Api.API_TOKEN, response.data.token);
        dispatch({ type: ACTION_TYPES.setLoggedIn });
        history.push("/");
      }
    });
  };

  const logout = () => {
    Api.logout();
    dispatch({ type: ACTION_TYPES.setLoggedOut });
    console.log("Log out");
    history.push("/login");
  };

  return (
    <div className="container hideMeOnPrint">
      <header style={{ minHeight: "54px", maxHeight: "6vh" }}>
        <div className="displayFlex">
          <h3 style={{ paddingLeft: "var(--universal-padding)" }}>
            {window.config.longInstanceName}
          </h3>
          {Api.loggedIn() && (
            <>
              <Link className="button" to={TAB.BOOK}>
                <Trans>Book appointments</Trans>
              </Link>
              <Link className="button" to={TAB.BOOKED}>
                <Trans>My appointments</Trans>
              </Link>
              <Link className="button" to={TAB.SETTINGS}>
                <Trans>Settings</Trans>
              </Link>
              <div className="flexAlignRight">
                <input
                  type="button"
                  value={i18n._(t`Logout`)}
                  onClick={logout}
                />
              </div>
            </>
          )}
        </div>
      </header>
      <Switch>
        <Route exact path="/">
          <Redirect to={TAB.BOOK} />
        </Route>
        <Route path="/login">
          <LoginView login={login} />
        </Route>
        <Route path={TAB.BOOK}>
          <BookView
            i18n={i18n}
            i18n={i18n}
            focusOnList={focusOnList}
            freeSlotList={freeSlotList}
            coupons={coupons}
            claimAppointment={claimAppointment}
            setSelectedAppointment={setSelectedAppointment}
            selectedAppointment={selectedAppointment}
            showSpinner={showSpinner}
            refreshList={refreshList}
            infoboxState={infoboxState}
            bookedAppointment={bookedAppointment}
            onBook={onBook}
            onCancelBooking={onCancelBooking}
            claimToken={claimToken}
            startDateTime={startDateTime}
            form={form}
            inputRef={inputRef}
          />
        </Route>
        <Route path={TAB.BOOKED}>
          <BookingHistoryView
            i18n={i18n}
            bookedList={bookedList}
            startDate={startDate}
            setStartDate={setStartDate}
            endDate={endDate}
            errorMessage={bookingHistoryErrorMessage}
            setEndDate={setEndDate}
            onDeleteBooking={onDeleteBooking}
          />
        </Route>
        <Route path={TAB.SETTINGS}>
          <SettingsView onSuccess={logout} />
        </Route>
      </Switch>
    </div>
  );
}

export default App;
