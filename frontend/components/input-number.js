import React, {useState} from "react";

export default function InputField({fieldName, placeholder, fieldType, name, required, handleChange, id}) {

 return (
   <div className="form-group row m-b-10">
     <label className="col-lg-3 text-lg-right col-form-label">
       {fieldName}

       {required && <span className="text-danger">*</span>}
     </label>
     <div className="col-lg-9 col-xl-6">
       <input id={id} type={fieldType} name={name} placeholder={placeholder} className="form-control" onChange={handleChange}/>
     </div>
   </div>
 )
}