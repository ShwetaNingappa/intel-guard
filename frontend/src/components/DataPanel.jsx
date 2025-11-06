import React from 'react';
import {
  Box,
  Text,
  VStack,
  HStack,
  Table,
  Tbody,
  Tr,
  Td,
  Badge,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from '@chakra-ui/react';

const DataPanel = ({ reputation, geolocation, ownership }) => {
  return (
    <Box p={6} borderWidth="1px" borderRadius="lg" bg="gray.800" borderColor="gray.700" shadow="lg">
      <Accordion allowMultiple defaultIndex={[0]}>
        {/* Reputation Data */}
        <AccordionItem borderColor="gray.700">
          <h2>
            <AccordionButton _hover={{ bg: 'gray.700' }}>
              <Box flex="1" textAlign="left">
                <Text fontSize="lg" fontWeight="bold" color="white">
                  Reputation Intelligence
                </Text>
              </Box>
              <AccordionIcon color="white" />
            </AccordionButton>
          </h2>
          <AccordionPanel pb={4} bg="gray.900">
            <VStack align="stretch" spacing={3}>
              <HStack justify="space-between">
                <Text fontWeight="medium" color="gray.300">AbuseIPDB Score:</Text>
                <Badge
                  colorScheme={
                    reputation.abuseipdb_score > 75
                      ? 'red'
                      : reputation.abuseipdb_score > 25
                      ? 'yellow'
                      : 'green'
                  }
                  fontSize="md"
                  px={3}
                  py={1}
                >
                  {reputation.abuseipdb_score ?? 'N/A'}
                </Badge>
              </HStack>
              <HStack justify="space-between">
                <Text fontWeight="medium" color="gray.300">Reports:</Text>
                <Text color="gray.200">{reputation.abuseipdb_reports?.length ?? 0} recent</Text>
              </HStack>
            </VStack>
          </AccordionPanel>
        </AccordionItem>

        {/* Geolocation Data */}
        <AccordionItem borderColor="gray.700">
          <h2>
            <AccordionButton _hover={{ bg: 'gray.700' }}>
              <Box flex="1" textAlign="left">
                <Text fontSize="lg" fontWeight="bold" color="white">
                  Geolocation & Network
                </Text>
              </Box>
              <AccordionIcon color="white" />
            </AccordionButton>
          </h2>
          <AccordionPanel pb={4} bg="gray.900">
            <Table size="sm" variant="simple">
              <Tbody>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">Country (IP-API):</Td>
                  <Td color="gray.200" borderColor="gray.700">{geolocation.ip_api_country ?? 'Unknown'}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">Country (IPStack):</Td>
                  <Td color="gray.200" borderColor="gray.700">{geolocation.ipstack_country ?? 'Unknown'}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">ISP (IP-API):</Td>
                  <Td color="gray.200" borderColor="gray.700">{geolocation.ip_api_isp ?? 'Unknown'}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">ISP (IPStack):</Td>
                  <Td color="gray.200" borderColor="gray.700">{geolocation.ipstack_isp ?? 'Unknown'}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">Hosting/Datacenter:</Td>
                  <Td borderColor="gray.700">
                    <Badge colorScheme={geolocation.consensus_hosting_flag ? 'orange' : 'blue'}>
                      {geolocation.consensus_hosting_flag ? 'Yes' : 'No'}
                    </Badge>
                  </Td>
                </Tr>
              </Tbody>
            </Table>
          </AccordionPanel>
        </AccordionItem>

        {/* Ownership Data */}
        <AccordionItem borderColor="gray.700">
          <h2>
            <AccordionButton _hover={{ bg: 'gray.700' }}>
              <Box flex="1" textAlign="left">
                <Text fontSize="lg" fontWeight="bold" color="white">
                  Ownership & WHOIS
                </Text>
              </Box>
              <AccordionIcon color="white" />
            </AccordionButton>
          </h2>
          <AccordionPanel pb={4} bg="gray.900">
            <Table size="sm" variant="simple">
              <Tbody>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">Registrar:</Td>
                  <Td color="gray.200" borderColor="gray.700">{ownership.whoisxml_registrar ?? 'Unknown'}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">Organization:</Td>
                  <Td color="gray.200" borderColor="gray.700">{ownership.whoisxml_organization ?? 'Unknown'}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">Admin Email:</Td>
                  <Td color="gray.200" borderColor="gray.700">{ownership.whois_admin_email ?? 'Not Available'}</Td>
                </Tr>
                <Tr>
                  <Td fontWeight="medium" color="gray.300" borderColor="gray.700">Historical Records:</Td>
                  <Td color="gray.200" borderColor="gray.700">{ownership.securitytrails_historical_count ?? 0}</Td>
                </Tr>
              </Tbody>
            </Table>
          </AccordionPanel>
        </AccordionItem>
      </Accordion>
    </Box>
  );
};

export default DataPanel;
