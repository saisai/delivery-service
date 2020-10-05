import React, {useState} from "react";
import SelectComponent from "../../select_component";
import {fetchAddressFromServer} from "../../../lib/data_fetch";
import InputField from "../../input-number";

export default function Step2(props) {
  const [district, setDistrict] = useState(null)
  const [street, setStreet] = useState(null)
  const [districtDefault, setDistrictOption] = useState(null)
  const [streetDefault, setStreetOption] = useState(null)
  const [foundAddresses, setFoundAddresses] = useState([])
  const [house, setHouse] = useState('')
  const [flat, setFlat] = useState('')
  const [addressFrom, setAddressFrom] = useState({})
  const [additionalInfo, setAddInfo] = useState({ ransomSum: 0})
  const [deliverySum, setDeliverySum] = useState(0)
  const [floor, setFloor] = useState('')

  const floorChange = (e) => {
    let floor = e.target.value;
    setFloor(floor);
    saveAddressTo({floor: floor});
  }

  const changeDeliverySum = (e) => {
    let deliverySum = e.target.value;
    setDeliverySum(deliverySum);
    saveAddressTo({delivery_sum: deliverySum});
  }

  const houseChange = (e) => {
    let houseNumber = e.target.value;
    setHouse(houseNumber);
    saveAddressTo({house: houseNumber})
  }

  const flatChange = (e) => {
    let flatNumber = e.target.value;
    setFlat(flatNumber);
    saveAddressTo({flat: flatNumber});
  }

  const saveAddressTo = (updateItem) => {
    let address = {
      ...addressFrom,
      ...updateItem,
    }
    setAddressFrom(address);
    props.changeAddressTo(address);
  }

  const streetsOptions = props.streets.map((street) => {
    return {value: street.id, label: street.name}
  })

  const districtOptions = props.districts.map((district) => {
    return {value: district.id, label: district.name}
  })

  const changeDistrict = (districtId) => {
    setDistrict(districtId);
    saveAddressTo({district: districtId});
  }

  const changeStreet = (streetId) => {
    setStreet(streetId)
    saveAddressTo({street:streetId})
  }

  const fetchAddress = (e) => {
    if (e.target.value.length > 0) {
      fetchAddressFromServer(e.target.value).then((data) => {
        setFoundAddresses(data)
      })
    } else {
      setFoundAddresses({})
    }
  }

  const selectAddress = (addr) => {
    let streetOption = {value: addr.street.id, label: addr.street.name};
    let districtOption = {value: addr.district.id, label: addr.district.name};
    setStreetOption(streetOption);
    setDistrictOption(districtOption);
    setHouse(addr.house);
    setFlat(addr.flat);
    saveAddressTo({
      district: addr.district.id,
      street: addr.street.id,
      house: addr.house,
      flat: addr.flat
    });
    document.getElementById('found-address').value = '';
    setFoundAddresses({});
  }

  const validateStepData = () => {
    return true
  }

  return (
    <div className='col-xl-4 col-lg-6 ui-sortable'>
        <div className="panel panel-inverse">
          <div className='panel-heading ui-sortable-handle'>
            <h4 className="panel-title">Введите адрес доставки</h4>
          </div>
          <div className='panel-body bg-light'>
            <div className='slimScrollDiv' style={{position: "relative", overflow: "hidden", width: "auto"}}>
              <InputField
                fieldName={"Имя клиента"}
                placeholder={'Имя клиента'}
                fieldType={'text'}
                name={'firstname'}
                required={true}
                id={'username'}
              />

              <InputField
                fieldName={"Номер телефона"}
                placeholder={'700-00-00-00'}
                fieldType={'number'}
                name={'number'}
                required={true}
                id={'phone-number'}
              />

              <InputField
                handleChange={fetchAddress}
                fieldName={"Адрес в базе"}
                placeholder={'Freshbox'}
                fieldType={'text'}
                name={'number'}
                id={'found-address'}
              />
              {!!foundAddresses.length > 0 &&
              <div className='dropdown-menu dropdown-menu-right show'>
                <div>
                  {foundAddresses.map((addr, index) =>
                    <div style={{display: "flex", justifyContent: 'center'}} key={index}>
                      <a className="dropdown-item" key={index} onClick={() => selectAddress(addr)}>
                        {addr.custom_name}
                        <small> &nbsp; Адресс: {addr.district.name} {addr.street.name} {addr.house ? addr.house : ''}</small>
                      </a>
                    </div>
                  )}
                </div>
              </div>
              }
            </div>

            <div className="form-group row m-b-10">
              <label className="col-lg-3 text-lg-right col-form-label"><strong>Район</strong> <span
                className="text-danger">*</span></label>
              <SelectComponent
                options={districtOptions}
                changeFunction={changeDistrict}
                placeHolder={'Район'}
                defaultInputValue={districtDefault}
              />
            </div>

            <div className="form-group row m-b-10">
              <label className="col-lg-3 text-lg-right col-form-label"><strong>Улица</strong> <span
                className="text-danger">*</span></label>
              <SelectComponent
                options={streetsOptions}
                changeFunction={changeStreet}
                placeHolder={'Улица'}
                defaultInputValue={streetDefault}
              />
            </div>

            <div>
              <div>
                <div className="form-group row m-b-10">
                  <label className="col-lg-3 text-lg-right col-form-label">Номер дома </label>
                  <div className="">
                    <input type="text" name="house" placeholder="" className="form-control" value={house}
                           onChange={houseChange}/>
                  </div>
                </div>

                <div className="form-group row m-b-10">
                  <label className="col-lg-3 text-lg-right col-form-label">Номер квартиры </label>
                  <div className="">
                    <input type="number" name="flat" placeholder="" onChange={flatChange} value={flat}
                           className="form-control"/>
                  </div>
                </div>
              </div>

              <div>
                <div className="form-group row m-b-10">
                  <label className="col-lg-3 text-lg-right col-form-label">Этаж </label>
                  <div className="">
                    <input type="number" name="flat" placeholder="" onChange={floorChange} value={floor}
                           className="form-control"/>
                  </div>
                </div>

                <div className="form-group row m-b-10">
                  <label className="col-lg-3 text-lg-right col-form-label">Домофон </label>
                  <div className="">
                    <input type="number" name="flat" placeholder="" className="form-control"/>
                  </div>
                </div>
              </div>

              <div className="form-group row m-b-10">
                <label className="col-lg-3 text-lg-right col-form-label"><strong>Сумма доставки </strong></label>
                <div className="col-lg-2 col-xl-2">
                  <input type="number" name="ransomSum" onChange={changeDeliverySum} value={deliverySum} className="form-control"/>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
  )
}