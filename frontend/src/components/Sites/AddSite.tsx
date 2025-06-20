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

import { type SiteCreate, SitesService } from "@/client"
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

const AddSite = () => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isValid, isSubmitting },
  } = useForm<SiteCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      name: "",
      latitude: 0,
      longitude: 0,
      model: "",
      line_in: "",
      line_out: "",
      polygon: "",
      username: "",
      password: "",
      host: "",
      port: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: SiteCreate) =>
      SitesService.createSite({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Site created successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["sites"] })
    },
  })

  const onSubmit: SubmitHandler<SiteCreate> = (data) => {
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
        <Button value="add-site" my={4}>
          <FaPlus fontSize="16px" />
          Add Site
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add Site</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Fill in the details to add a new site.</Text>
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
              <Field
                required
                invalid={!!errors.line_in}
                errorText={errors.line_in?.message}
                label="Line In"
              >
                <Input
                  id="line_in"
                  {...register("line_in", {
                    required: "Line In is required.",
                  })}
                  placeholder="Line In"
                  type="text"
                />
              </Field>
              <Field
                required
                invalid={!!errors.line_out}
                errorText={errors.line_out?.message}
                label="Line Out"
              >
                <Input
                  id="line_out"
                  {...register("line_out", {
                    required: "Line Out is required.",
                  })}
                  placeholder="Line Out"
                  type="text"
                />
              </Field>
              <Field
                required
                invalid={!!errors.polygon}
                errorText={errors.polygon?.message}
                label="Polygon"
              >
                <Input
                  id="polygon"
                  {...register("polygon", {
                    required: "Polygon is required.",
                  })}
                  placeholder="Polygon"
                  type="text"
                />
              </Field>
              <Field
                required
                invalid={!!errors.username}
                errorText={errors.username?.message}
                label="Username"
              >
                <Input
                  id="username"
                  {...register("username", {
                    required: "Username is required.",
                  })}
                  placeholder="Username"
                  type="text"
                />
              </Field>
              <Field
                required
                invalid={!!errors.password}
                errorText={errors.password?.message}
                label="Password"
              >
                <Input
                  id="password"
                  {...register("password", {
                    required: "Password is required.",
                  })}
                  placeholder="Password"
                  type="text"
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

export default AddSite
