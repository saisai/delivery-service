import React, {useEffect, useState} from "react";
import WorkingShiftModal from "./workingShiftModal";
import {endOperatorShift, startOperatorShift} from "../../lib/shift";

export default function StartEndShiftModal(props) {
  const [modalShow, setModalShow] = useState(false);
  const [errors, setShiftErrors] = useState([]);
  const [showStartShift, setShowStartShift] = useState(false);
  const [showEndShift, setShowEndShift] = useState(false);

  useEffect(() => {
    console.log("aAAAAA")
    if (props.errors.length > 0 && errors !== props.errors) {
      console.log("BBBBBB")
      setShiftErrors(props.errors)
      setModalShow(true);
      setShowEndShift(true);
    }
    else if (props.operator.start_time === null) {
      console.log("CCCCCCCCCC")
      setModalShow(true);
      setShowStartShift(true);
    }
  }, [props.errors])

  function Show() {
    setModalShow(true);
  }

  function hideModal() {
    setModalShow(false)
  }

  function handleStartShift() {
    console.log('handleStartShift')
    startOperatorShift().then((data) => {
      props.setOperatorShift(data);
    })
  }

  function handleEndShift() {
    endOperatorShift().then((data) => {
      props.clearErrors();
    })
  }


  return (
    <WorkingShiftModal
      show={modalShow}
      handleEndShift={handleEndShift}
      handleStartShift={handleStartShift}
      onHide={hideModal}
      showStartShiftButton={showStartShift}
      showEndShiftButton={showEndShift}
    />
  )
}