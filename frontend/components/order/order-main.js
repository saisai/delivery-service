import Step1 from "./order-steps/step_1";
import Step2 from "./order-steps/step_2";
import Step3 from "./order-steps/step_3";
import React from "react";


export default function OrderdMain(props) {
  const {
    streets,
    cities,
    districts,
    changeAddressFrom,
    changeAddressTo,
    setAdditionalInfo,
    setCourier,
    couriers,
  } = props;

  return (
    <div className='row'>
      <Step1
        streets={streets}
        cities={cities}
        districts={districts}
        changeAddressFrom={changeAddressFrom}
        setAdditionalInfo={setAdditionalInfo}
      />
      <Step2
        streets={streets}
        cities={cities}
        districts={districts}
        changeAddressTo={changeAddressTo}
        setAdditionalInfo={setAdditionalInfo}
      />
      <Step3
        setCourier={setCourier}
        setAdditionalInfo={setAdditionalInfo}
        couriers={couriers}
      />
    </div>
  )
}