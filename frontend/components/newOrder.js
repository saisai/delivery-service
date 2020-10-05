import React, {useEffect, useState} from "react";
import CreateOrderModal from "./order/create-order-modal";


export default function NewOrder({cities, districts, streets, couriers}) {
  const [modalShow, setModalShow] = useState(false);

  function Show() {
    setModalShow(true);
  }

  function hideModal() {
    setModalShow(false)
  }

  return (
    <>
      <button className="btn btn-primary btn-block m-b-5" onClick={Show}>
        Оформить заказ
      </button>

      <CreateOrderModal
        show={modalShow}
        onHide={hideModal}
        cities={cities}
        districts={districts}
        streets={streets}
        couriers={couriers}
      />
    </>
  );
}