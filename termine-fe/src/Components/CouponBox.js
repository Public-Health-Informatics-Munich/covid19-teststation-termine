import React from "react";

export const CouponBox = ({ coupons }) => {
  return (
    <div id="coupons">
      <h3 style={{ paddingLeft: "calc(2 * var(--universal-padding))" }}>
        {coupons > 0 ? (
          <div>
            Sie können noch{" "}
            <b>
              <u>{coupons} Termine</u>
            </b>{" "}
            vergeben.
          </div>
        ) : coupons === 0 ? (
          <>
            <div>
              Sie können{" "}
              <b>
                <u>keine Termine</u>
              </b>{" "}
              mehr vergeben.
            </div>
            <div
              dangerouslySetInnerHTML={{
                __html: window.config.contactInfoCoupons,
              }}
            />
          </>
        ) : (
          <div>&nbsp;</div>
        )}
      </h3>
    </div>
  );
};
