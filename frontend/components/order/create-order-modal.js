import React, {useState} from "react";
import {makeOrder} from "../../lib/order";
import OrderMain from "./order-main";


export default function CreateOrderModal(
  {
    show,
    onHide,
    cities,
    districts,
    streets,
    couriers
  }
) {
  const [addressFrom, setAddressFrom] = useState({});
  const [addressTo, setAddressTo] = useState({});
  const [additionalInfo, setAdditionalInfo] = useState({});
  const [orderCourier, setOrderCourier] = useState(null);
  const [client, setClient] = useState({});
  const [errors, setErrors] = useState(null);

  function changeAddressFrom(address) {
    setAddressFrom(address)
  }

  function changeAddressTo(address) {
    setAddressTo(address)
  }

  function setCourierToOrder(courierId) {
    setOrderCourier(courierId)
  }

  function setAdditionalOrderInfo(additionalInfo) {
    setAdditionalInfo(additionalInfo)
  }

  function close() {
    onHide()
  }

  function createOrder() {
    let payload = {
      addressFrom: addressFrom,
      addressTo: addressTo,
      additionalInfo: additionalInfo,
      courier: orderCourier,
      client: client
    }
    if (addressFrom.street && addressFrom.district && orderCourier) {
      makeOrder(payload).then((data) => {
        console.log(data)
      })
      close();
    }
    setErrors("Не все обязательные поля заполнены")
  }

  return (
    <>
      {show &&
      <div className="modal modal-message fade show" id="modal-message"
           style={{display: "block", paddingRight: "15px"}} aria-modal="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h4 className="modal-title">Создать заказ</h4>
              <button type="button" className="close" data-dismiss="modal" aria-hidden="true" onClick={close}>×</button>
            </div>
            <div className="modal-body">

              <OrderMain
                streets={streets}
                cities={cities}
                districts={districts}
                changeAddressFrom={changeAddressFrom}
                changeAddressTo={changeAddressTo}
                couriers={couriers}
                setCourier={setCourierToOrder}
                setAdditionalInfo={setAdditionalOrderInfo}
              />
            { errors &&
              <div>
                <span style={{color: "red"}}>* {errors} </span>
              </div>
            }
            </div>

            <div className="modal-footer">
              <a className="btn btn-white" data-dismiss="modal" onClick={close}>Close</a>
              <a className="btn btn-primary" onClick={createOrder}>Save Changes</a>
            </div>

          </div>
        </div>
      </div>
      }
    </>
  );
}
