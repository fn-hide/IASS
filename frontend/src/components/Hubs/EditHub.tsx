import {
  Button,
  ButtonGroup,
  DialogActionTrigger,
  Input,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaExchangeAlt } from "react-icons/fa"

import { type ApiError, type HubPublic, HubsService } from "@/client"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog"
import { Field } from "../ui/field"

interface EditHubProps {
  hub: HubPublic
}

interface HubUpdateForm {
  name: string | null
  address: string | null
  latitude: number | null
  longitude: number | null
  host: string | null
  port: string | null
  sync_interval: number | null
  sync_size: number | null
  model: string | null
}

const EditHub = ({ hub }: EditHubProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<HubUpdateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      ...hub,
      address: hub.address ?? undefined,
      latitude: hub.latitude ?? null,
      longitude: hub.longitude ?? null,
      host: hub.host ?? undefined,
      port: hub.port ?? undefined,
      sync_interval: hub.sync_interval ?? null,
      sync_size: hub.sync_size ?? null,
      model: hub.model ?? undefined,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: HubUpdateForm) =>
      HubsService.updateHub({ id: hub.id, requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Hub updated successfully.")
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

  const onSubmit: SubmitHandler<HubUpdateForm> = async (data) => {
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
        <Button variant="ghost">
          <FaExchangeAlt fontSize="16px" />
          Edit Hub
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Hub</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the hub details below.</Text>
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
                invalid={!!errors.sync_size}
                errorText={errors.sync_size?.message}
                label="Synchronize limit"
              >
                <Input
                  id="sync_size"
                  {...register("sync_size", {
                    required: "Synchronize limit is required.",
                  })}
                  placeholder="Synchronize limit"
                  type="number"
                />
              </Field>
              <Field
                required
                invalid={!!errors.sync_interval}
                errorText={errors.sync_interval?.message}
                label="Health check interval"
              >
                <Input
                  id="sync_interval"
                  {...register("sync_interval", {
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
            <ButtonGroup>
              <DialogActionTrigger asChild>
                <Button
                  variant="subtle"
                  colorPalette="gray"
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>
              </DialogActionTrigger>
              <Button variant="solid" type="submit" loading={isSubmitting}>
                Save
              </Button>
            </ButtonGroup>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default EditHub
