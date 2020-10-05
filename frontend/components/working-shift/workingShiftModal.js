import OrderMain from "../order/order-main";
import React from "react";
import classNames from "classnames";

export default function WorkingShiftModal(
  {
    show,
    onHide,
    handleStartShift,
    handleEndShift,
    showStartShiftButton,
    showEndShiftButton,
  }) {

  const disableStartButton = showEndShiftButton ? 'disabled' : ''
  const disableEndButton = showStartShiftButton ? 'disabled' : ''

  const startButtonClassNames = classNames({
    'btn btn-block m-b-5': true,
    'btn-warning': showStartShiftButton,
    'btn-default disabled disable-pointer': showEndShiftButton,
  })
  const endButtonClassNames = classNames({
    'btn btn-block m-b-5': true,
    'btn-warning': showEndShiftButton,
    'btn-default disabled disable-pointer': showStartShiftButton,
  })

  const endShift = () => {
    if (!disableEndButton) {
      handleEndShift();
    }
  }

  const startShift = () => {
    if (!disableStartButton) {
      handleStartShift();
    }
  }

  return (
    <>
      {show &&
      <div className="modal modal-message fade show" id="modal-message"
           style={{display: "block", paddingRight: "15px"}} aria-modal="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h4 className="modal-title">Начать/Закончить смену</h4>
            </div>
            <div className="modal-body">
              <div className="d-sm-flex align-items-center m-b-10">
                <div className={`col-xl-5`}>
                  <button className={startButtonClassNames} onClick={startShift}>
                    Начать смену
                  </button>
                </div>
                <div className={`col-xl-5 `}>
                  <button className={endButtonClassNames} onClick={endShift}>
                    Закончить смену
                  </button>
                </div>
              </div>

            </div>

          </div>
        </div>
      </div>
      }
    </>
  )
}