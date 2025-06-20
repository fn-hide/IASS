import { IconButton } from "@chakra-ui/react"
import { BsThreeDotsVertical } from "react-icons/bs"
import { MenuContent, MenuRoot, MenuTrigger } from "../ui/menu"

import type { HubPublic } from "@/client"
import DeleteHub from "../Hubs/DeleteHub"
import EditHub from "../Hubs/EditHub"

interface HubActionsMenuProps {
  hub: HubPublic
}

export const HubActionsMenu = ({ hub }: HubActionsMenuProps) => {
  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <IconButton variant="ghost" color="inherit">
          <BsThreeDotsVertical />
        </IconButton>
      </MenuTrigger>
      <MenuContent>
        <EditHub hub={hub} />
        <DeleteHub id={hub.id} />
      </MenuContent>
    </MenuRoot>
  )
}
