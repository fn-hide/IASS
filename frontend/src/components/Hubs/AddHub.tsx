import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"

import {
  Button,
  DialogActionTrigger,
  DialogTitle,
  Input,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useState } from "react"
import { FaPlus } from "react-icons/fa"

import { type HubCreate, HubsService } from "@/client"
import type { ApiError } from "@/client/core/ApiError"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTrigger,
} from "../ui/dialog"
import { Field } from "../ui/field"

const AddHub = () => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isValid, isSubmitting },
  } = useForm<HubCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      name: "",
      address: "",
      latitude: 0,
      longitude: 0,
      host: "",
      port: "",
      limit_send: 0,
      interval_ping: 0,
      model: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: HubCreate) =>
      HubsService.createHub({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Hub created successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["hubs"] })
    },
  })

  const onSubmit: SubmitHandler<HubCreate> = (data) => {
    mutation.mutate(data)
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "md" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger asChild>
        <Button value="add-hub" my={4}>
          <FaPlus fontSize="16px" />
          Add Hub
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add Hub</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Fill in the details to add a new hub.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.name}
                errorText={errors.name?.message}
                label="Name"
              >
                <Input
                  id="name"
                  {...register("name", {
                    required: "Name is required.",
                  })}
                  placeholder="Name"
                  type="text"
                />
              </Field>
              <Field
                required
                invalid={!!errors.address}
                errorText={errors.address?.message}
                label="Address"
              >
                <Input
                  id="address"
                  {...register("address", {
                    required: "Address is required.",
                  })}
                  placeholder="Address"
                  type="text"
                />
              </Field>
              <Field
                required
                invalid={!!errors.latitude}
                errorText={errors.latitude?.message}
                label="Latitude"
              >
                <Input
                  id="latitude"
                  {...register("latitude", {
                    required: "Latitude is required.",
                  })}
                  placeholder="Latitude"
                  type="number"
                />
              </Field>
              <Field
                required
                invalid={!!errors.longitude}
                errorText={errors.longitude?.message}
                label="Longitude"
              >
                <Input
                  id="longitude"
                  {...register("longitude", {
                    required: "Longitude is required.",
                  })}
                  placeholder="Longitude"
                  type="number"
                />
              </Field>
              <Field
                required
                invalid={!!errors.host}
                errorText={errors.host?.message}
                label="Host"
              >
                <Input
                  id="host"
                  {...register("host", {
                    required: "Host is required.",
                  })}
                  placeholder="Host"
                  type="text"
                />
              </Field>
              <Field
                required
                invalid={!!errors.port}
                errorText={errors.port?.message}
                label="Port"
              >
                <Input
                  id="port"
                  {...register("port", {
                    required: "Port is required.",
                  })}
                  placeholder="Port"
                  type="text"
                />
              </Field>
              <Field
                required
                invalid={!!errors.limit_send}
                errorText={errors.limit_send?.message}
                label="Synchronize limit"
              >
                <Input
                  id="limit_send"
                  {...register("limit_send", {
                    required: "Synchronize limit is required.",
                  })}
                  placeholder="Synchronize limit"
                  type="number"
                />
              </Field>
              <Field
                required
                invalid={!!errors.interval_ping}
                errorText={errors.interval_ping?.message}
                label="Health check interval"
              >
                <Input
                  id="interval_ping"
                  {...register("interval_ping", {
                    required: "Health check interval is required.",
                  })}
                  placeholder="Health check interval"
                  type="number"
                />
              </Field>
              <Field
                required
                invalid={!!errors.model}
                errorText={errors.model?.message}
                label="Model"
              >
                <Input
                  id="model"
                  {...register("model", {
                    required: "Model is required.",
                  })}
                  placeholder="Model"
                  type="text"
                />
              </Field>
            </VStack>
          </DialogBody>

          <DialogFooter gap={2}>
            <DialogActionTrigger asChild>
              <Button
                variant="subtle"
                colorPalette="gray"
                disabled={isSubmitting}
              >
                Cancel
              </Button>
            </DialogActionTrigger>
            <Button
              variant="solid"
              type="submit"
              disabled={!isValid}
              loading={isSubmitting}
            >
              Save
            </Button>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default AddHub
