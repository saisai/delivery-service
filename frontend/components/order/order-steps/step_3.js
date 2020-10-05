import React, {useEffect, useState} from "react";
import SelectComponent from "../../select_component";


export default function Step3(props) {
  const [couriers, setCouriers] = useState([])
  const [courierOption, setCourierOption] = useState({})
  const [commentText, setCommentText] = useState({})

  const couriersOptions = props.couriers.map((courier, index) => {
    return {value: courier.id, label: courier.courier.username}
  })

  const changeCourier = (option) => {
    setCourierOption(option);
    props.setCourier(option)
  }

  const changeText = (e) => {
    let comment = e.target.value;
    setCommentText(comment);
    console.log(comment)
    props.setAdditionalInfo({comment: comment})
  }

  return (
    <div className='col-xl-4 col-lg-6 ui-sortable'>
      <div className="panel panel-inverse">
        <div className='panel-heading ui-sortable-handle'>
          <h4 className="panel-title">Назначить на курьера</h4>
        </div>
        <div className='panel-body bg-light'>
          <div className="form-group row m-b-10">
            <label className="col-lg-3 text-lg-right col-form-label"><strong>Выбрать курьера</strong>
              <span className="text-danger">*</span>
            </label>
            <SelectComponent
              options={couriersOptions}
              changeFunction={changeCourier}
              placeHolder={'Куреры'}
            />
          </div>
        </div>
      </div>
      <div className="panel panel-inverse">
        <div className='panel-heading ui-sortable-handle'>
          <h4 className="panel-title">Коментарий к заказу</h4>
        </div>
        <div className='panel-body bg-light'>
            <textarea
              id="console" rows="20"
              className="form-control"
              placeholder=""
              spellCheck="false"
              onChange={changeText}
            />

        </div>
      </div>

    </div>
  )
}