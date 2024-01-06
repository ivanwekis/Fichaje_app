from fastapi import HTTPException
from app.controllers.main.models.register import Register, Input, Output


def get_registers_lenght(mongo_users, mongo_collections, user):
    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        return {"registers_length": mongo_collections.registers_length()}
    else:
        raise HTTPException(
            status_code=404, detail="There was an error getting the registers length."
        )


def get_registers(page, mongo_users, mongo_collections, user):
    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        registers_doc = mongo_collections.find_12_sort_by_date({}, page)

        registers_list = []
        for register_doc in registers_doc:
            register = Register()
            register.string_id = register_doc["string_id"]
            register.date = register_doc["date"]
            register.inputs = register_doc["inputs"]
            register.outputs = register_doc["outputs"]
            if "modified" in register_doc:
                register.modified = register_doc["modified"]
            if "nightShift" in register_doc:
                register.nightShift = register_doc["nightShift"]
            registers_list.append(register.dict())
        return {"registers": registers_list}
    else:
        raise HTTPException(status_code=403, detail="Incorrect username.")


def modify_register(mongo_users, mongo_collections, user, register):
    output_list = []
    input_list = []
    for output in register.outputs:
        output_obj = Output()
        output_obj.output = output.output
        output_obj.reason = output.reason
        output_list.append(output_obj.dict())
    for input in register.inputs:
        input_obj = Input()
        input_obj.input = input.input
        input_list.append(input_obj.dict())

    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        if mongo_collections.update_one_register(
            {"string_id": register.string_id},
            {"inputs": input_list, "outputs": output_list, "modified": True},
        ):

            return {"message": "The register has been modified successfully."}
        else:
            raise HTTPException(
                status_code=404,
                detail="The register does not exist or the id is incorrect.",
            )

    else:
        raise HTTPException(status_code=403, detail="Incorrect username.")
