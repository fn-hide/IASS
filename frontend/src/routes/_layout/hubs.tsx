import {
  Container,
  EmptyState,
  Flex,
  Heading,
  Table,
  VStack,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { FiSearch } from "react-icons/fi"
import { z } from "zod"

import { HubsService } from "@/client"
import { HubActionsMenu } from "@/components/Common/HubActionsMenu"
import AddHub from "@/components/Hubs/AddHub"
import PendingItems from "@/components/Pending/PendingItems"
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination.tsx"

const hubsSearchSchema = z.object({
  page: z.number().catch(1),
})

const PER_PAGE = 5

function getHubsQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      HubsService.readHubs({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
    queryKey: ["hubs", { page }],
  }
}

export const Route = createFileRoute("/_layout/hubs")({
  component: Hubs,
  validateSearch: (search) => hubsSearchSchema.parse(search),
})

function HubsTable() {
  const navigate = useNavigate({ from: Route.fullPath })
  const { page } = Route.useSearch()

  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getHubsQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  })

  const setPage = (page: number) =>
    navigate({
      search: (prev: { [key: string]: string }) => ({ ...prev, page }),
    })

  const hubs = data?.data.slice(0, PER_PAGE) ?? []
  const count = data?.count ?? 0

  if (isLoading) {
    return <PendingItems />
  }

  if (hubs.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>You don't have any hubs yet</EmptyState.Title>
            <EmptyState.Description>
              Add a new hub to get started
            </EmptyState.Description>
          </VStack>
        </EmptyState.Content>
      </EmptyState.Root>
    )
  }

  return (
    <>
      <Table.Root size={{ base: "sm", md: "md" }}>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader w="sm">ID</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Name</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Address</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Latitude</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Longitude</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Host</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Port</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Sync Limit</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Check Interval</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Model</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {hubs?.map((hub) => (
            <Table.Row key={hub.id} opacity={isPlaceholderData ? 0.5 : 1}>
              <Table.Cell truncate maxW="sm">
                {hub.id}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.name}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.address}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.latitude}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.longitude}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.host}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.port}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.limit_send}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.interval_ping}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {hub.model}
              </Table.Cell>
              <Table.Cell>
                <HubActionsMenu hub={hub} />
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
      <Flex justifyContent="flex-end" mt={4}>
        <PaginationRoot
          count={count}
          pageSize={PER_PAGE}
          onPageChange={({ page }) => setPage(page)}
        >
          <Flex>
            <PaginationPrevTrigger />
            <PaginationItems />
            <PaginationNextTrigger />
          </Flex>
        </PaginationRoot>
      </Flex>
    </>
  )
}

function Hubs() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Hubs Management
      </Heading>
      <AddHub />
      <HubsTable />
    </Container>
  )
}
