import React from 'react';
import {
  Box,
  Text,
  VStack,
  HStack,
  Icon,
  Badge,
  Divider,
} from '@chakra-ui/react';
import { WarningIcon } from '@chakra-ui/icons';

const NewsCampaigns = ({ campaigns }) => {
  if (!campaigns || campaigns.length === 0) {
    return (
      <Box
        p={6}
        borderWidth="1px"
        borderRadius="lg"
        bg="gray.800"
        borderColor="gray.700"
        shadow="lg"
      >
        <VStack align="stretch" spacing={3}>
          <HStack>
            <Icon as={WarningIcon} color="orange.400" boxSize={5} />
            <Text fontSize="lg" fontWeight="bold" color="white">
              Threat Intelligence News
            </Text>
          </HStack>
          <Text color="gray.400" fontSize="sm">
            No related campaigns or news found for this IP.
          </Text>
        </VStack>
      </Box>
    );
  }

  return (
    <Box
      p={6}
      borderWidth="1px"
      borderRadius="lg"
      bg="gray.800"
      borderColor="orange.500"
      shadow="lg"
    >
      <VStack align="stretch" spacing={4}>
        <HStack justify="space-between">
          <HStack>
            <Icon as={WarningIcon} color="orange.400" boxSize={5} />
            <Text fontSize="lg" fontWeight="bold" color="white">
              Related Threat Campaigns & News
            </Text>
          </HStack>
          <Badge colorScheme="orange" fontSize="xs" px={2} py={1}>
            ACTIVE THREATS
          </Badge>
        </HStack>

        <Divider borderColor="gray.700" />

        <VStack align="stretch" spacing={3}>
          {campaigns.map((campaign, index) => (
            <Box
              key={index}
              p={4}
              bg="gray.900"
              borderRadius="md"
              borderLeft="4px"
              borderColor="orange.400"
              _hover={{
                bg: 'gray.750',
                transform: 'translateX(4px)',
                transition: 'all 0.2s'
              }}
            >
              <HStack align="start" spacing={3}>
                <Box
                  minW="24px"
                  h="24px"
                  borderRadius="full"
                  bg="orange.500"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  color="white"
                  fontSize="xs"
                  fontWeight="bold"
                  mt={1}
                >
                  {index + 1}
                </Box>
                <Text color="gray.100" fontSize="sm" lineHeight="tall">
                  {campaign}
                </Text>
              </HStack>
            </Box>
          ))}
        </VStack>

        <Box
          p={3}
          bg="orange.900"
          borderRadius="md"
          borderLeft="3px"
          borderColor="orange.500"
        >
          <Text fontSize="xs" color="orange.200" fontWeight="medium">
            ⚠️ These campaigns are identified by AI based on IP infrastructure patterns and known threat intelligence.
          </Text>
        </Box>
      </VStack>
    </Box>
  );
};

export default NewsCampaigns;
