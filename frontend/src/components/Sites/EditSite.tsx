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

import { type ApiError, type SitePublic, SitesService } from "@/client"
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

interface EditSiteProps {
  site: SitePublic
}

interface SiteUpdateForm {
  name: string | null
  latitude: number | null
  longitude: number | null
  model: string | null
  username: string | null
  password: string | null
  host: string | null
  port: string | null
  line_in: string | null
  line_out: string | null
  polygon: string | null
}

const EditSite = ({ site }: EditSiteProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<SiteUpdateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      ...site,
      latitude: site.latitude ?? null,
      longitude: site.longitude ?? null,
      model: site.model ?? undefined,
      line_in: site.line_in ?? undefined,
      line_out: site.line_out ?? undefined,
      polygon: site.polygon ?? undefined,
      username: site.username ?? undefined,
      password: site.password ?? undefined,
      host: site.host ?? undefined,
      port: site.port ?? undefined,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: SiteUpdateForm) =>
      SitesService.updateSite({ id: site.id, requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Site updated successfully.")
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

  const onSubmit: SubmitHandler<SiteUpdateForm> = async (data) => {
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
          Edit Site
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Site</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the site details below.</Text>
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
                  step="any"
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
                  step="any"
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

export default EditSite
